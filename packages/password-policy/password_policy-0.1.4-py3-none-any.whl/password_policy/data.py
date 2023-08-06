from __future__ import annotations

from dataclasses import field
from typing import Any, Optional

# Use pydantic for type checking. It is slower, but not much of an issue for parsing.
from pydantic.dataclasses import dataclass

import json
import itertools

from string import ascii_lowercase, ascii_uppercase, digits, punctuation

#region Helper functions

def _to_json_compatible_object(obj: dataclass) -> dict[str,Any]:
  """
  Converts arbitrary objects to json suitable objects. Tries to convert types intelligently.

  Args:
      obj (Any): Object to convert to json.

  Returns:
      dict[str,Any]: Object suitable for use with ``json.dumps``.
  """
  data = {}
  
  for name, value in obj.__dict__.items():
    # Filter out private variables
    if name.startswith('_'):
      continue
    
    # Filter out empty fields
    if value is None or (hasattr(value, '__len__') and len(value) == 0):
      continue
    
    # Convert non-json compatible types
    if isinstance(value, set):
      value = list(value)
    elif isinstance(value, PCPSubsetRequirement):
      value = _to_json_compatible_object(value)
    elif isinstance(value, dict) and any(filter(lambda x: isinstance(x, PCPCharsetRequirement), value.values())):
      value = { key: _to_json_compatible_object(requirement) for key, requirement in value.items() }
      
    # Write value to data object
    data[name] = value
  
  return data


def _uses_alphabet_charset(rules: list[PCPRule]) -> bool:
  """
  Checks if the given rules use the alphabet charset.

  Args:
      rules (list[PCPRule]): List of rules to check.

  Returns:
      bool: Whether the rules use the alphabet charset.
  """
  for rule in rules:
    if rule.require is not None and 'alphabet' in rule.require:
      return True
    if rule.require_subset is not None and rule.require_subset.options is not None and 'alphabet' in rule.require_subset.options:
      return True
    if rule.charset_requirements is not None and 'alphabet' in rule.charset_requirements:
      return True
  return False

#endregion

#region PCP

DEFAULT_CHARSETS: dict[str,str] = {
  "lower": ascii_lowercase,
  "upper": ascii_uppercase,
  "digits": digits,
  "symbols": punctuation  
}

ALPHABET_CHARSETS: dict[str,str] = {
  "alphabet": ascii_lowercase + ascii_uppercase,
  "digits": digits,
  "symbols": punctuation  
}

@dataclass()
class PCP():
  """
  Password composition policy (PCP).

  ``rules`` is the set of rules making up the PCP. As long as one rule matches, the password will be accepted.
  
  ``charsets`` is the list of supported character sets. By default, includes upper, lower, digits, and symbols. Character sets can be redefined, but character sets must not overlap. An empty character set cannot be a part of a PCP.
  """
  rules: list[PCPRule]
  charsets: dict[str,str] = field(default_factory=DEFAULT_CHARSETS.copy)
  
  def dumps(self) -> str:
    """Create a json representation of this object.

    Returns:
        str: Representation of this object in json.
    """
    
    # Simplified outputs if features not used
    if self.charsets == DEFAULT_CHARSETS or self.charsets == ALPHABET_CHARSETS:
      if len(self.rules) == 1:
        return json.dumps(_to_json_compatible_object(self.rules[0]))
      else:
        return json.dumps({'rules': [_to_json_compatible_object(rule) for rule in self.rules]})

    # Get a diff between the defined charset and the default charset. Only dump this diff.
    charsets_diff: dict[str,str] = {}
    default_charset = ALPHABET_CHARSETS if 'alphabet' in self.charsets else DEFAULT_CHARSETS
        
    for name, charset in self.charsets.items():
      if name not in default_charset or set(charset) != set(default_charset[name]):
        charsets_diff[name] = charset
    
    for name in default_charset.keys():
      if name not in self.charsets:
        charsets_diff[name] = None
    
    return json.dumps({'charsets': charsets_diff, 'rules': [_to_json_compatible_object(rule) for rule in self.rules]})
    
    
  @staticmethod
  def loads(s: str) -> PCP:
    """
    Load a PCP object from a json string.

    Args:
        s (str): String to parse.

    Returns:
        PCP: PCP object parsed from the string.
    """
    data = json.loads(s)
    
    # Parse the rules
    rules: list[PCPRule]
    if 'rules' not in data or data['rules'] is None:
      rules = [PCPRule._from_json(data)]
    else:
      rules = [PCPRule._from_json(rule) for rule in data['rules']]
    
    # Parse the charsets
    charsets: dict[str, str] = ALPHABET_CHARSETS.copy() if _uses_alphabet_charset(rules) else DEFAULT_CHARSETS.copy()
    if 'charsets' in data and data['charsets'] is not None:
      for key, value in data['charsets'].items():
        if value is None or len(value) == 0:
          charsets.pop(key)
        else:
          charsets[key] = value
      
    # Create and return the object
    return PCP(rules, charsets)
    
  def validate(self) -> None:
    """
    Validates that the policy is self consistent.

    Raises:
        ValueError: Describes how the policy is malformed.
    """
        
    for key, value in self.charsets.items():
      if len(value) == 0:
        raise ValueError(f'charsets[{key}] must not be empty')
    for charset1, charset2 in itertools.combinations(self.charsets.keys(), 2):
      if not set(self.charsets[charset1]).isdisjoint(set(self.charsets[charset2])):
        raise ValueError(f'charsets[{charset1}] and charsets[{charset2}] may not have shared characters')
    
    if len(self.rules) < 1:
      raise ValueError(f'rules must contain at least one rule')
    for i in range(len(self.rules)):
      self.rules[i]._validate(f'rules[{i}]', set(self.charsets.keys()))
      
    # TODO: Validate that min_length and max_length make sense with all the other rules.
  
#endregion

#region PCPRule

@dataclass()
class PCPRule():
  """
  Rule that a password must conform to.
  
  ``min_length`` is the minimum number of characters in the password. Must be 1 or higher.
  ``max_length`` is the maximum number of characters in the password.
  ``max_consecutive`` is the maximum number of consecutive identical characters allowed.
  ``prohibited_substrings`` is a list of substrings not allowed in the password.
  
  ``require`` is the list of charsets that must appear in the password.
  ``require_subset`` is a list of charsets for which sum number must appear in the password.
  
  ``charset_requirements`` is the set of additional requirements for each charset.
  """
  min_length: int = 1
  max_length: Optional[int] = None
  max_consecutive: Optional[int] = None
  prohibited_substrings: Optional[set[str]] = None
  
  require: Optional[set[str]] = None
  require_subset: Optional[PCPSubsetRequirement] = None
  
  charset_requirements: Optional[dict[str,PCPCharsetRequirement]] = None
  
  @staticmethod
  def _from_json(data: dict[str,Any]) -> PCPRule:
    """
    Load a PCPRule from a json-compatible object.

    Args:
        data (dict[str,Any]): Object to parse.

    Returns:
        PCPRule: Parsed PCPRule.
    """
    if 'prohibited_substrings' in data and data['prohibited_substrings'] is not None:
      data['prohibited_substrings'] = set(data['prohibited_substrings'])
    if 'require' in data and data['require'] is not None:
      data['require'] = set(data['require'])
    if 'require_subset' in data and data['require_subset'] is not None:
      data['require_subset'] = PCPSubsetRequirement._from_json(data['require_subset'])
    if 'charset_requirements' in data and data['charset_requirements'] is not None:
      data['charset_requirements'] = {
        key: PCPCharsetRequirement._from_json(value) 
        for key, value in data['charset_requirements'].items() 
      }
    return PCPRule(**data)
    
  def _validate(self, argname: str, charsets: set[str]) -> None:
    """
    Validates that the rule is self consistent.

    Args:
        argname (str): Name of this object within the policy.
        charsets (set[str]): Charsets defined by the policy.

    Raises:
        ValueError: Describes how the policy is malformed.
    """
    
    if self.min_length < 1:
      raise ValueError(f'{argname}.min_length may not be less than 1')
    if self.max_length is not None and self.max_length < 1:
      raise ValueError(f'If set, {argname}.max_length may not be less than 1')
    if self.max_length is not None and self.min_length is not None and self.max_length < self.min_length:
      raise ValueError(f'{argname}.max_length cannot be less than min_length')
    if self.max_consecutive is not None and self.max_consecutive < 1:
      raise ValueError(f'If set, {argname}.max_consecutive may not be less than 1')
    
    if self.require is not None and not self.require.issubset(charsets):
        raise ValueError(f'{argname}.require includes invalid charsets ({self.require - charsets.keys()})')
    if self.require_subset is not None:
      self.require_subset._validate(f'{argname}.subset_requirement', charsets)
    
    if self.charset_requirements is not None:
      for key, value in self.charset_requirements.items():
        if key not in charsets:
          raise ValueError(f'{argname}.charset_requirements[{key}] is not a valid charset name')
        value._validate(f'{argname}.charset_requirements[{key}]', self.min_length)
  
    # Check that require and require_subset don't overlap with each other
    require_charsets = self.require or set()
    subset_charsets = self.require_subset.options or charsets if self.require_subset else set()
    if len(require_charsets.intersection(subset_charsets)) > 0:
      raise ValueError(f'In {argname}, require, require_subset, and charset_requirements cannot have overlapping charset requirements ({require_charsets.intersection(subset_charsets)})') 
    
    # Check that charset_requirements are all valid
    if self.charset_requirements is not None:
      for key, value in self.charset_requirements.items():
        # Check overlap with require and require_subset
        if (key in require_charsets or key in subset_charsets):
          if value.min_required is not None:
            raise ValueError(f'In {argname}, require, require_subset, and charset_requirements cannot have overlapping charset requirements ({key})')
          if value.max_allowed is not None and value.max_allowed == 0:
            raise ValueError(f'In {argname}, charset_requirements[{key}].max_allowed cannot be 0 when the charset is used in require or require_subset')
        
#endregion

#region PCPSubsetRequirement

@dataclass()
class PCPSubsetRequirement():
  """
  Requirement that some number of the selected character must exist in the password.
  
  ``count`` is the number of charsets from the options list that must appear in the password.
  ``options`` is the set of character sets from which characters must be selected. If unset, all charsets will be used as valid options.
  """
  count: int
  options: Optional[set[str]] = None
  
  @staticmethod
  def _from_json(data: dict[str,Any]) -> PCPSubsetRequirement:
    """Load a PCPSubsetRequirement from a json-compatible object.

    Args:
        data (dict[str,Any]): Object to parse.

    Returns:
        PCPSubsetRequirement: Parsed PCPSubsetRequirement.
    """
    if 'options' in data and data['options'] is not None:
      data['options'] = set(data['options'])
    return PCPSubsetRequirement(**data)
    
  def _validate(self, argname: str, charsets: set[str]) -> None:
    """Validates that the subset requirement is self consistent.

    Args:
        argname (str): Name of this object within the policy.
        charsets (set[str]): Charsets defined by the policy.

    Raises:
        ValueError: Describes how the policy is malformed.
    """
    if self.count < 1:
      raise ValueError(f'{argname}.count may not be less than 1')
    if self.options is None:
      if self.count >= len(charsets):
        raise ValueError(f'{argname}.count may not be greater than or equal to the number of available character sets')
    else:
      if len(self.options) < 2:
        raise ValueError(f'{argname}.options must include at least two charsets')
      if not self.options.issubset(charsets):
        raise ValueError(f'{argname}.options includes invalid charsets ({self.options - charsets.keys()})')
      if self.count >= len(self.options):
        raise ValueError(f'{argname}.count may not be greater than or equal to the number of options')

#endregion

#region PCPCharsetRequirement

@dataclass()
class PCPCharsetRequirement():
  """
  Additional requirements for a charset within a given rule.
  
  ``min_required`` is the minimum number of characters from the associated charset needed in the password.
  ``max_allowed`` is the maximum number of characters from the associated charset allowed in the password.
  ``max_consecutive`` is the maximum number of consecutive characters from this charset allowed.
  ``required_locations`` is a list of positions within the password that must use this character set. 0-based indexing, with support for negative indexes.
  ``prohibited_locations`` is a list of positions within the password that must not use this character set. 0-based indexing, with support for negative indexes.
`` locations, indexing matches python string indexing.
  """
  min_required: Optional[int] = None
  max_allowed: Optional[int] = None
  max_consecutive: Optional[int] = None
  required_locations:  Optional[set[int]] = None
  prohibited_locations: Optional[set[int]] = None

  @staticmethod
  def _from_json(data: dict[str,Any]) -> PCPCharsetRequirement:
    """
    Load a PCPCharsetRequirement from a json-compatible object.

    Args:
        data (dict[str,Any]): Object to parse.

    Returns:
        PCPCharsetRequirement: Parsed PCPCharsetRequirement.
    """
    if 'required_locations' in data and data['required_locations'] is not None:
      data['required_locations'] = set(data['required_locations'])
    if 'prohibited_locations' in data and data['prohibited_locations'] is not None:
      data['prohibited_locations'] = set(data['prohibited_locations'])    
    return PCPCharsetRequirement(**data)
    
  def _validate(self, argname: str, min_length: int) -> None:
    """
    Validates that the charset requirement is self consistent.

    Args:
        argname (str): Name of this object within the policy.

    Raises:
        ValueError: Describes how the policy is malformed.
    """
    if self.min_required is not None and self.min_required < 1:
      raise ValueError(f'If set, {argname}.min_required may not be less than 1')
    if self.max_allowed is not None and self.max_allowed < 1:
      raise ValueError(f'If set, {argname}.max_allowed may not be less than 1')
    if self.max_consecutive is not None and self.max_consecutive < 1:
      raise ValueError(f'If set, {argname}.max_consecutive may not be less than 1')
    
    if self.required_locations is not None:
      for location in self.required_locations:
        if (location >= 0 and location >= min_length) or (location < 0 and (-location + 1) >= min_length):
            raise ValueError(f'{argname}.required_locations contains a location ({location}) that is not guaranteed to exist in the password given its min_length')
    
    if self.required_locations is not None and self.prohibited_locations is not None and \
        len(self.required_locations.intersection(self.prohibited_locations)) > 0:
      raise ValueError(f'{argname}.required_locations and prohibited_locations may not overlap')

    if self.max_allowed is not None:
      if self.min_required is not None and self.max_allowed < self.min_required:
        raise ValueError(f'{argname}.max_allowed cannot be less than min_required')
      if self.required_locations is not None and len(self.required_locations) > self.max_allowed:
        raise ValueError(f'{argname}.required_locations cannot be more than max_allowed')
      

#endregion

PCP.__pydantic_model__.update_forward_refs()
PCPRule.__pydantic_model__.update_forward_refs()
PCPSubsetRequirement.__pydantic_model__.update_forward_refs()
PCPCharsetRequirement.__pydantic_model__.update_forward_refs()
