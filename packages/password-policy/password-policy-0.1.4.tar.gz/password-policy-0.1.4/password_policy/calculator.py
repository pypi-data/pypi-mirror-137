from __future__ import annotations

import functools
import itertools

from dataclasses import dataclass, field
from typing import Callable, Iterator, Optional, TypeVar

from .data import PCP, PCPRule  

#region Helper methods

from math import factorial as _math_factorial
_factorial = functools.lru_cache(_math_factorial)

T = TypeVar('T')
def _apply(f: Callable[[T,T],T], lhs: Optional[T], rhs: Optional[T]) -> Optional[T]:
  """
  Apply the given function if both elements are not ``None``. Otherwise return the non-``None`` item.

  Args:
      f (Callable[[T,T],T]): Function to apply if both value are not ``None``.
      lhs (T): First value.
      rhs (T): Second value.

  Returns:
      T: Resulting value.
  """
  if lhs is None:
    if rhs is None: return None
    else: return rhs
  else:
    if rhs is None: return lhs
    else: return f(rhs, lhs)

#endregion

#region CompositionGenerator
      
@dataclass(frozen=True)
class CompositionGenerator:
  """
  Generator for ``PasswordComposition`` objects.
  
  ``length`` is the length of password compositions to generate.
  ``required`` is the number of characters required for each charset.
  ``max_allowed`` is them maximum number of characters allowed for each charset.
  """
  length: int
  required: list[int]
  max_allowed: list[Optional[int]]
  
  def compositions(self, preferences: list[int] = []) -> Iterator[Composition]:
    """
    Yields the compositions for this generator.

    Args:
        preferences (list[int], optional): List of charsets to prefer when generating compositions. Defaults to [].

    Yields:
        Iterator[PasswordComposition]: Compositions of the given length.
    """
    required_length = sum(self.required)
    remaining_length = self.length - required_length
    remaining_characters: list[list[int]] = []
    
    # Compute which characters can still appear in the password
    for i in range(remaining_length):
      allowed_charsets = []
    
      for j in range(len(self.max_allowed)):
        if self.max_allowed[j] is None or self.max_allowed[j] > self.required[j] + i:
          allowed_charsets.append(j) 
        
        # If using preferences, limit allowed_charsets to first available preferred charset.
        for preference in preferences:
          if preference in allowed_charsets:
            allowed_charsets = [preference]
            break
      
      remaining_characters.append(allowed_charsets)
    
    # Now we need to generate the compositions
    for charset_combinations in itertools.product(*remaining_characters):
      composition = self.required.copy()
      for i in charset_combinations:
        composition[i] += 1
      yield Composition(composition)
      
      
  def __hash__(self):
    return self.length ^ hash(tuple(self.required)) ^ hash(tuple(self.max_allowed))
      
#endregion

#region CompositionRestrictions

@dataclass(frozen=True)
class CompositionRestrictions:
  """
  Restrictions for compositions when calculating permutations.
  
  ``max_consecutive_characters`` is the max consecutive same characters allowed.
  ``prohibited_substrings`` is the set of substrings that can't appear in the password.
  ``charsets_max_consecutive`` is the list of max_consecutive characters for each charset.
  ``charsets_required_locations`` is the list of required_locations characters for each charset.
  ``charsets_prohibited_locations`` is the list of prohibited_locations characters for each charset.
  """
  max_consecutive: Optional[int] = None
  prohibited_substrings: Optional[set[prohibitedSubstring]] = None
  charsets_max_consecutive: Optional[list[Optional[int]]] = None
  charsets_required_locations: Optional[list[Optional[set[int]]]] = None
  charsets_prohibited_locations: Optional[list[Optional[set[int]]]] = None

  @staticmethod
  def merge(lhs: CompositionRestrictions, rhs: CompositionRestrictions) -> CompositionRestrictions:
    """
    Merge two CompositionRestrictions objects.
    
    It is unclear how to best do this. There are two approaches, with their associated limitations:
      (1) Keep track of both sets of restrictions seperately, calculating search space separately. The limitation with this method is that for nearly all real-world policies this would lead to significant overlap in the two search spaces (overestimating strength). The only way to compensate for this would be to enumerate the actual permutations, but this is not tractable.
      (2) Create a new restriction object that represents only the restrictions that are common between both, calculating the search space for this new restriction only. The limitation with this method is that it will count passwords that would fail both options. This will lead to an overstimate of the search space.
      
      Ultimately, we use (2) because it is faster and because we believe the overestimation to be much smaller. In fact, this will only be a problem for very complicated policies, none of which we have seen in practice. Also, for basic merges (2) will give the correct answers.

    Args:
        lhs (CompositionRestrictions): First object to merge.
        rhs (CompositionRestrictions): Second object to merge.

    Returns:
        CompositionRestrictions: Merged composition restriction.
    """
    
    # Use the larger of the two consecutive character counts
    if lhs.max_consecutive is None:
      max_consecutive = rhs.max_consecutive
    elif not rhs.max_consecutive is None:
      max_consecutive = max(lhs.max_consecutive, rhs.max_consecutive)
      
    # Use prohibited strings that are in both sets
    if lhs.prohibited_substrings is None:
      prohibited_substrings = rhs.prohibited_substrings
    elif rhs.prohibited_substrings is not None:
      prohibited_substrings = lhs.prohibited_substrings | rhs.prohibited_substrings
    
    # Use the larger of the two charset consecutive character counts
    if lhs.charsets_max_consecutive is None:
      charsets_max_consecutive = rhs.charsets_max_consecutive
    elif rhs.charsets_max_consecutive is not None:
      charsets_max_consecutive = [
        _apply(max, lhs, rhs) for lhs, rhs in zip(lhs.charsets_max_consecutive, rhs.charsets_max_consecutive)
      ]
    
    # Use the intersection of the required locations
    if lhs.charsets_required_locations is None:
      charsets_required_locations = rhs.charsets_required_locations
    elif rhs.charsets_required_locations is not None:
      charsets_required_locations = [
        _apply(set.intersection, lhs, rhs)
        for lhs, rhs in zip(lhs.charsets_required_locations, rhs.charsets_required_locations)
      ]
      
    # Use the intersection of the prohibited locations
    if lhs.charsets_prohibited_locations is None:
      charsets_prohibited_locations = rhs.charsets_prohibited_locations
    elif rhs.charsets_prohibited_locations is not None:
      charsets_prohibited_locations = [
        _apply(set.intersection, lhs, rhs)
        for lhs, rhs in zip(lhs.charsets_prohibited_locations, rhs.charsets_prohibited_locations)
      ]
      
    return CompositionRestrictions(max_consecutive, prohibited_substrings,
                                   charsets_max_consecutive, charsets_required_locations, charsets_prohibited_locations)
  
  
  def __hash__(self):
    return hash(self.max_consecutive) ^ \
      hash(tuple(self.prohibited_substrings or [])) ^ \
      hash(tuple(self.charsets_max_consecutive or [])) ^ \
      hash(tuple(self.charsets_required_locations or [])) ^ \
      hash(tuple(self.charsets_prohibited_locations or [])) 
    

@dataclass(frozen=True)
class prohibitedSubstring:
  """
  Represents a prohibited substring. Keeps track of both the actual string (needed for de-duplication) and the charset composition of that string.
  """
  substring: str
  composition: list[int] = field(compare=False, hash=False)
  
  
#endregion

#region Composition
    
@dataclass(frozen=True)
class Composition():
  """
  Represents the composition of a password in terms of charsets.

  ``composition`` is a list of how many characters from each charset make up this composition.
  """
  composition: list[int]
  
  def get_search_space(self, 
                       restrictions_set: set[CompositionRestrictions], 
                       charset_sizes: list[int]) -> int:
    """
    Get the search space for this composition.

    Return value will be exact for composition without restrictions, compositions with a single restriction, and for some simple combination of restrictions. Otherwise, the resulting search space will be smaller than it should be as restrictions will be remoed multiple times. The only way to solve this is to expand combinations and/or permutations, but this is not tractable.

    Args:
        restrictions_set (set[CompositionRestrictions]): Set of restrictions for valid passwords.
        charset_sizes (list[int]): How many characters are in each charset of the composition.

    Returns:
        int: Estimate of the search space for this composition. 
    """
    return max(0, self._get_search_space(restrictions_set, charset_sizes))
  
  
  def _get_search_space(self, 
                       restrictions_set: set[CompositionRestrictions], 
                       charset_sizes: list[int]) -> int: 
    """"""
    # If no restrictions, just return the  basic search space calculation
    if restrictions_set is None or len(restrictions_set) == 0:
      return self._get_simple_search_space(charset_sizes)
    
    # Handle restrictions.
    restrictions = functools.reduce(CompositionRestrictions.merge, restrictions_set)
    
    # For required locations, we calculate the search space based on those charsets being in a fixed location.
    search_space: int
    
    if restrictions.charsets_required_locations is not None:
      new_composition = self.composition.copy()
      location_counts = [0] * len(self.composition)
      
      for i in range(0, len(self.composition)):
        if restrictions.charsets_required_locations[i] is not None:
          location_count = len(restrictions.charsets_required_locations[i])

          # Not enough occurrences to satisfy required positions
          if location_count > new_composition[i]:
            return 0

          new_composition[i] -= location_count
          location_counts[i] = location_count
      
      search_space = Composition(new_composition)._get_simple_search_space(charset_sizes)
      for i in range(len(location_counts)):
        search_space *= (charset_sizes[i] ** location_counts[i])

    else:
      search_space = self._get_simple_search_space(charset_sizes)
    
    # For each of the remaining restrictions, we create a combination that explicitly violates the restriction, measure its search space, then remove that amount from our existing search space calculation. If multiple restrictions are in place, this will overestimate the number of restrictions being removed. Restrictions are considered individually. As such, overlap is not handled correctly---i.e., we will end up underestimating the search space as combinations/permutations could be removed multiple times. Still, this effect should be small. More importantly, complex policies that would cause this problem are likely extremely rare, as none exist in the dataset used to create this PCP library.
    
    # 1) Handle max_consecutive. If a charset has more possible occurrences than max_allowed, remove (max_allowed+1) occurrences from that charset and replace them with a single occurrence of a new charset representing a single character from the charset being repeated (max_allowed+1) times. Deduct the search space of this new (invalid) composition from the overall search space.
    if restrictions.max_consecutive is not None:
      for i in range(0, len(self.composition)):
        if self.composition[i] > restrictions.max_consecutive:
          
          if  restrictions.charsets_max_consecutive is not None and \
              restrictions.charsets_max_consecutive[i] is not None and \
              restrictions.charsets_max_consecutive[i] <= restrictions.max_consecutive:
            continue
          
          new_composition = self.composition.copy()
          new_composition[i] -= (restrictions.max_consecutive + 1)
          new_composition.append(1)
          
          new_charset_sizes = charset_sizes.copy()
          new_charset_sizes.append(charset_sizes[i])
          
          search_space -= Composition(new_composition)._get_simple_search_space(new_charset_sizes)
    
    
    # 2) Handle charset_max_consecutive. If a charset has more possible occurrences than chatset_max_allowed[i], remove (max_allowed+1) occurrences from that charset and replace them with a single occurrence of a new charset representing a combination of characters from that charset of length (max_allowed+1). Deduct the search space of this new (invalid) composition from the overall search space.
    if restrictions.charsets_max_consecutive is not None:
      for i in range(0, len(self.composition)):
        if restrictions.charsets_max_consecutive[i] is not None:
          max_consecutive = restrictions.charsets_max_consecutive[i]
          
          if self.composition[i] > max_consecutive:
            new_composition = self.composition.copy()
            new_composition[i] -= (max_consecutive + 1)
            new_composition.append(1)
            
            new_charset_sizes = charset_sizes.copy()
            new_charset_sizes.append(charset_sizes[i] ** (max_consecutive + 1))
            
            search_space -= Composition(new_composition)._get_simple_search_space(new_charset_sizes)
      
          
    # 3) Handle prohibited_substrings. These substrings are represented by the charsets needed to represent them. If sufficient charset occurrences are available, remove them and replace with a single charset representing the prohibited substring. Deduct the search space of this new (invalid) composition from the overall search space.
    if restrictions.prohibited_substrings is not None:
      for substring in restrictions.prohibited_substrings:
        if all([available >= required for available, required in zip(self.composition, substring.composition)]):
          new_composition = [
            available - required for available, required in zip(self.composition, substring.composition)
          ]
          new_composition.append(1)
          
          new_charset_sizes = charset_sizes.copy()
          new_charset_sizes.append(1)
          
          search_space -= Composition(new_composition)._get_simple_search_space(new_charset_sizes)
          
          
    # 4) Handle prohibited_locations. For each prohibited location, we remove one occurrence for that charset and calculate how many combinations/permutations are possible for the other characters. We then remove this number for each possible violating character in the given position.
    if restrictions.charsets_prohibited_locations is not None:
      for i in range(0, len(self.composition)):
        if restrictions.charsets_prohibited_locations[i] is not None:
          # If we can't violate the prohibition, we don't need to worry about it
          if self.composition[i] == 0: continue
          
          for _ in restrictions.charsets_prohibited_locations[i]:
            new_composition = self.composition.copy()
            new_composition[i] -= 1

            new_search_space = Composition(new_composition)._get_simple_search_space(charset_sizes)
            search_space -= (new_search_space * charset_sizes[i])
          
    return search_space
  
  
  def _get_simple_search_space(self, charset_sizes: list[int]) -> int:
    """Get the search space for the given composition. Does not consider composition restrictions.

    Args:
        charset_sizes (list[int]): How many characters make up each charset.

    Returns:
        int: The search space for the given composition.
    """
    space: int = 1
    
    # Calculate combinations
    for i in range(len(self.composition)):
      space *= (charset_sizes[i] ** self.composition[i])
    
    # Calculate unique permutations of the combinations
    space *= _factorial(sum(self.composition))
    for count in self.composition:
      space //= _factorial(count)
      
    return space
  
  
  def __hash__(self):
    return hash(tuple(self.composition)) 

#endregion

#region Strength calculator

DEFAULT_CHARSET_PREFERENCES = ['lower', 'upper', 'alphabet', 'digits', 'symbols']


def get_machine_strength(pcp: PCP) -> int:
  """Get the strength of machine-generated passwords for the given the policy. Assumes (1) the machine picks the shortest possible password, (2) machines use as many charsets as allowed, and (3) on average the adversary will guess the password after guessing half the passwords.

  Args:
      pcp (PCP): Policy for which to measure strength.

  Returns:
      int: The average number of guesses needed to find a password created for the given policy.
  """
  return _get_strength(pcp)

  
def get_human_strength(pcp: PCP, charset_preferences: list[str] = DEFAULT_CHARSET_PREFERENCES) -> int:
  """Get the strength of human-generated passwords for the given the policy. Assumes (1) users pick the shortest possible password, (2) users pick their preferred charsets when available, and (3) on average the adversary will guess the password after guessing half the passwords.

  Args:
      pcp (PCP): Policy for which to measure strength.
      charset_preferences (list[str], optional): Which charsets the user prefers to use if available, in order. Defaults to DEFAULT_CHARSET_PREFERENCES.

  Returns:
      int: The average number of guesses needed to find a password created for the given policy.
  """
  return _get_strength(pcp, charset_preferences)


def _get_strength(pcp: PCP, charset_preferences: list[str] = []) -> int:
  """Get the strength of the given policy. Assumes (1) the shortest possible password will be used, (2) charsets will be used based on the given preference (if any), and (3) on average the adversary will guess the password after guessing half the passwords.

  Args:
      pcp (PCP): Policy for which to measure strength.
      charset_preferences (list[str], optional): Which charsets are preferred to use if available, in order. Defaults to DEFAULT_CHARSET_PREFERENCES.

  Returns:
      int: The average number of guesses needed to find a password created for the given policy.
  """
  
  # Ensure we have a valid pcp as we assume the policies are well formed
  pcp.validate()
  
  # Map the charsets to integers. More efficient to process
  charset_mapping = { name: index for name, index in zip(sorted(pcp.charsets.keys()), range(len(pcp.charsets))) }
  charset_sizes = [len(pcp.charsets[key]) for key in charset_mapping.keys()]
  preferences = [charset_mapping[preference] for preference in charset_preferences if preference in charset_mapping]
  
  # Get the set of password compositions produced by the policy. Also keep track of restrictions for each composition.
  compositions: dict[Composition, set[CompositionRestrictions]] = dict()
  for generator, restrictions_set in get_generators(pcp, charset_mapping).items():
    for composition in generator.compositions(preferences):
      if not composition in compositions:
        compositions[composition] = set()
      if restrictions_set is not None:
        compositions[composition].update(restrictions_set)
        
  # Add up the search spaces for each composition. This works because compositions are distinct
  search_space = 0
  for composition, restrictions_set in compositions.items():
    search_space += composition.get_search_space(restrictions_set, charset_sizes)
    
  # On average, the password will be guessed when half the search space is exhausted
  return search_space // 2


def get_generators(pcp: PCP, charset_mapping: dict[str,int]) -> dict[CompositionGenerator,set[CompositionRestrictions]]:
  """[summary]

  Args:
      pcp (PCP): Policy for which to measure strength.
      charset_mapping (dict[str,int]): Mapping from charsets to indices.

  Returns:
      dict[CompositionGenerator, set[CompositionRestrictions]]: Generators with associated restrictions.
  """
  smallest_min_length = min([r.min_length for r in pcp.rules])
  generators: dict[CompositionGenerator, set[CompositionRestrictions]] = dict()
  
  for rule in filter(lambda r: r.min_length == smallest_min_length, pcp.rules):
    # Get PasswordCompositionGenerator relevant data from the rule 
    required: list[int] = [0] * len(charset_mapping)
    max_allowed: list[Optional[int]] = [None] * len(charset_mapping)
    
    try:
      restriction = _get_composition_restrictions(rule, pcp.charsets, charset_mapping)
    except ValueError as e:
      print('Rule at the given minimum length has restrictions that cannot be simultaneously met. Skipping.')
      print(e)
      print(rule)
      continue
        
    # Look at required characters in charset_requirements
    if rule.charset_requirements is not None:
      for charset, requirement in rule.charset_requirements.items():
        if requirement.min_required is not None:
          required[charset_mapping[charset]] = requirement.min_required
        if requirement.max_allowed is not None:
          max_allowed[charset_mapping[charset]] = requirement.max_allowed
    
    # Look at required characters in require
    if rule.require is not None:
      for charset in rule.require:
        required[charset_mapping[charset]] = 1
    
    # Look at required characters in require_subset. This is done by creating a different generator for each subset.
    def _add_to_generators(generator):
      if generator not in generators:
        generators[generator] = set()
      if restriction is not None:
        generators[generator].add(restriction)
    
    if rule.require_subset is not None:
      options = set(map(lambda x: charset_mapping[x], rule.require_subset.options or charset_mapping.keys()))
      for include in itertools.combinations(options, rule.require_subset.count):
        new_required = [max(1, required[index]) if index in include else required[index] 
                        for index in range(len(required))]        
        _add_to_generators(CompositionGenerator(rule.min_length, new_required, max_allowed))
    else:
      _add_to_generators(CompositionGenerator(rule.min_length, required, max_allowed)) 
      
  return generators
        

def _get_composition_restrictions(
  rule: PCPRule,
  charsets: dict[str,str],
  charset_mapping: dict[str,int]) -> Optional[CompositionRestrictions]:
  """
  Get a composition restriction object, if applicable, for the given rule.

  Args:
      rule (PCPRule): Rule to get restrictions from.
      charsets (dict[str,str]): Charsets defined by the policy.
      charset_mapping (dict[str,int]): Mapping from charsets to indices.

  Returns:
      Optional[CompositionRestrictions]: Restrictions, or ``None`` if there are none.
  """
  # Process prohibited substrings
  prohibited_substrings: Optional[set[prohibitedSubstring]] = None
  
  if rule.prohibited_substrings is not None:
    prohibited_substrings = set()
    
    for substring in rule.prohibited_substrings:
      composition = [0] * len(charsets)
      for char in substring:
        for name, charset in charsets.items():
          if char in charset:
            composition[charset_mapping[name]] += 1
            break
      prohibited_substrings.add(prohibitedSubstring(substring, composition))
  
  # Process charset_* restrictions
  charsets_max_consecutive: Optional[list[Optional[int]]] = None
  charsets_required_locations: Optional[list[Optional[set[int]]]] = None
  charsets_prohibited_locations: Optional[list[Optional[set[int]]]] = None
  
  if rule.charset_requirements is not None:    
    charsets_max_consecutive = [None] * len(charset_mapping)
    charsets_required_locations = [None] * len(charset_mapping)
    charsets_prohibited_locations = [None] * len(charset_mapping)
    
    # Tracks required locations to prevent overlap 
    is_required_location = [False] * len(charset_mapping)

    for charset in charset_mapping.keys():
      if charset in rule.charset_requirements:
        requirements = rule.charset_requirements[charset]
        index = charset_mapping[charset]
        
        charsets_max_consecutive[index] = requirements.max_consecutive

        # Convert negative indices
        if requirements.required_locations is not None:
          charsets_required_locations[index] = set()
          for location in requirements.required_locations:
            if location < 0: 
              location += rule.min_length
            charsets_required_locations[index].add(location)
            
            if is_required_location[index]:
              raise ValueError('Multiple charsets required at position {index}')
            else:
              is_required_location[index] = True
            
        # Convert negative indices
        if requirements.prohibited_locations is not None:
          charsets_prohibited_locations[index] = set()
          for location in requirements.prohibited_locations:
            if location < 0: 
              location += rule.min_length
            charsets_prohibited_locations[index].add(location)
            
        # Check to see that requirements is self consistent
        if charsets_required_locations[index] is not None and charsets_prohibited_locations is not None and \
            len(charsets_required_locations[index].intersection(charsets_prohibited_locations[index])) > 0:
          raise ValueError('Charset restrictions requires a character both be in and not be in the same location')

      # Check to see that requirements is self consistent
      

    # No need for empty restrictions
    if not any(charsets_max_consecutive):
      charsets_max_consecutive = None
    if not any(charsets_required_locations):
      charsets_required_locations = None
    if not any(charsets_prohibited_locations):
      charsets_prohibited_locations = None
    
  args = [rule.max_consecutive, prohibited_substrings,
          charsets_max_consecutive, charsets_required_locations, charsets_prohibited_locations]
  if not any(args):
    return None
  else:
    return CompositionRestrictions(*args)

#endregion
