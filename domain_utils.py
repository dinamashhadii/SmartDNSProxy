def normalize_domain(domain):
    domain = domain.strip().lower()
    if domain.endswith('.'):
        domain = domain[:-1]
    return domain
def is_valid_domain(domain):
    if not domain:
        return False
    if domain.endswith('.'):
        return False
    labels = domain.split('.')
    for label in labels:
        if len(label) == 0:
            return False
        if label.startswith('-') or label.endswith('-'):
            return False
        for char in label:
            if not (char.isascii() and (char.isalnum() or char == '-')):
                return False
    return True
def domain_match(domain,domain_list):
    for entry in domain_list:
        if domain == entry or domain.endswith("."+entry):
            return True
    return False