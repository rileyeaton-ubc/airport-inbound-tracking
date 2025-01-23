def roman_numerals_to_int(roman_num):
  true_roman = roman_num.upper()
  if true_roman == "I":
    return 1
  elif true_roman == "II":
    return 2
  elif true_roman == "III":
    return 3
  elif true_roman == "IV":
    return 4
  elif true_roman == "V":
    return 5
  elif true_roman == "VI":
    return 6
  else:
    return -1
