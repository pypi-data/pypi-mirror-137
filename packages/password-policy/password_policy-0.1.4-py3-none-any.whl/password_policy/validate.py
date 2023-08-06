from .data import PCP, PCPRule


def check_password(password: str, pcp: PCP) -> bool:
  """Checks whether the given password is valid for the given PCP.

  Args:
      password (str): Password to validate.
      pcp (PCP): PCP to validate against.

  Returns:
      bool: Whether the password is valid.
  """
  pcp.validate()
  password_length = len(password)
  
  # Map the password onto the charsets. Helpful when checking charset requirements.
  charset_mapping = { name: index for name, index in zip(sorted(pcp.charsets.keys()), range(len(pcp.charsets))) }
  password_mapped = []
  for char in password:
    found: bool = False
    
    for name, charset in pcp.charsets:
      if char in charset:
        password_mapped.append(charset_mapping[name])
        found = True
        break
    
    # Password uses a non-allowed character
    if not found:
      return False
        
  # Check each rule. Only one needs to pass for validation to succeed  
  for rule in pcp.rules:
    if (_check_password_against_rule(password, rule, password_length, charset_mapping, password_mapped)):
      return True  
          
  return False


def _check_password_against_rule(
  password: str, 
  rule: PCPRule, 
  password_length: int, 
  charset_mapping: dict[str,int], 
  password_mapped: list[int]) -> bool:
  """Checks whether the given password is valid for the given rules.

  Args:
      password (str): Password to validate.
      rule (PCPRule): Rule to validate against.
      password_length (int): Length of the password.
      charset_mapping (dict[str,int]): A mapping between charsets and indices.
      password_mapped (list[int]): The password mapped into the charset index for each character.

  Returns:
      bool: Whether the password is valid.
  """
  
  # min_length
  if password_length < rule.min_length:
    return False
  
  # max_length
  if rule.max_length is not None and password_length > rule.max_length:
    return False
  
  # max_consecutive
  if rule.max_consecutive is not None:
    last_char: str = ''
    consecutive_count: int = 0
    
    for char in password:
      if char == last_char:
        consecutive_count += 1
        if consecutive_count > rule.max_consecutive:
          return False
      else:
        last_char = char
        consecutive_count = 1
  
  # prohibited substrings
  if rule.prohibited_substrings is not None:
    for substring in rule.prohibited_substrings:
      if substring in password:
        return False
      
  # require
  if rule.require:
    for charset in rule.require:
      if not charset_mapping[charset] in password_mapped:
        return False
      
  # require subset
  if rule.require_subset is not None:
    options: list[int]
    if rule.require_subset.options is not None:
      options = [charset_mapping[charset] for charset in rule.require_subset.options]
    else:
      options = list(charset_mapping.values())
  
    option_matched = [1 if option in password_mapped else 0 for option in options]
    if sum(option_matched) < rule.require_subset.count:
      return False
    
  # charset requirements
  if rule.charset_requirements is not None:
    for charset, requirements in rule.charset_requirements.items():
      charset_index = charset_mapping[charset]
      charset_count = password_mapped.count(charset_index)
      
      # min required
      if requirements.min_required and charset_count < requirements.min_required:
        return False
      
      # max allowed
      if requirements.max_allowed and charset_count > requirements.max_allowed:
        return False
      
      # max consecutive
      if requirements.max_consecutive is not None:
        consecutive_count: int = 0
        
        for index in password_mapped:
          if index == charset_index:
            consecutive_count += 1
            if consecutive_count > requirements.max_consecutive:
              return False
          else:
            consecutive_count = 0
            
      # required locations
      if requirements.required_locations:
        for location in requirements.required_locations:
          if password_mapped[location] != charset_index:
            return False
      
      # prohibited locations
      if requirements.prohibited_locations:
        for location in requirements.prohibited_locations:
          # Ignored prohibited locations that don't exist in the string
          if (location >= 0 and location < password_length) or (location < 0 and (-location + 1) < password_length):
            if password_mapped[location] == charset_index:
              return False
  
  # Everything checks out
  return True
