def print_result(domain , source , status,ip,ttl):
    if domain == "":
        domain = "(empty)"
    if ip is None:
        ip = "-"
    if ttl is None:
        ttl = "-"
    print(f"Domain : {domain}")
    print(f"Source : {source}")
    print(f"Status : {status}")
    print(f"IP : {ip}")
    print(f"TTL : {ttl}")
    print()
def process_domain(user_domain,config,ad_domains,sanction_domain,cache):
    domain = user_domain.strip()
    if not is_valid_domain(domain):
        print_result(domain,"NONE","INVALID_INPUT",None,None)
        return
    domain = normalize_domain(domain)
    if domain_match(domain,ad_domains):
        print_result(domain,"AD_BLOCK","OK",config["sinkhole_ip"],config["local_ttl"])
        return
    if domain_match(domain,sanction_domain):
        print_result(domain,"SANCTION","OK",config["proxy_ip"],config["local_ttl"])
        return
    if config["cache_enabled"] :
        cache_result = get_cache(domain,cache)
        if cache_result is not None:
            ip,remaining_ttl = cache_result
            print_result(domain, "CACHE", "OK", ip, remaining_ttl)
            return
    status,ip,ttl = query_upstream(domain,config)
    if status == "SERVER_ERROR":
        print_result(domain,"UPSTREAM","SERVER_ERROR",None,None)
        return
    if status == "NOT_FOUND":
        print_result(domain,"UPSTREAM","NOT_FOUND",None,None)
        return
    if config["cache_enabled"] and ttl>0:
        save_cache(domain,ip,ttl,cache)
    print_result(domain,"UPSTREAM","OK",ip,ttl)
def main():
    try:
        config = config_txt()
        ad_domains = domain_list(config["ad_list_file"])
        sanction_domain = domain_list(config["sanction_list_file"])
    except (ValueError,OSError) as error:
        print(f"config error: {error}")
        return
    cache = {}
    print("DNS Proxy ready")
    while True:
        user_domain = input("Enter domain (or exit):")
        if user_domain.strip().lower() == 'exit':
            print("Bye")
            break
        process_domain(user_domain,config,ad_domains,sanction_domain,cache)
if __name__ == "__main__":main()