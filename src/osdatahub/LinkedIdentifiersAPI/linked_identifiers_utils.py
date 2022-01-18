
def validate_options(value, options):
    if value not in options.values:
        valid = "\n\t".join(options.values)
        raise ValueError(f"'{value}' is not a valid {options.name}, please choose from one of the following:\n\t{valid}")
    return True


if __name__ =="__main__":
    
    from osdatahub.LinkedIdentifiersAPI.linked_identifier_options import correlation_methods, feature_types
    
    validate_options("test", feature_types)