def keyword_creator(position, industry):
    # Process positions
    positions_list = [f'"{role.strip()}"' for role in position.split(",")]
    positions_query = " OR ".join(positions_list)

    # Process industries
    industries_list = [f'"{ind.strip()}"' for ind in industry.split(",")]
    industries_query = " AND ".join(industries_list)

    # Construct the final query
    query = f"{positions_query} {industries_query} -intitle:\"profiles\" -inurl:\"dir/ \" site:in.linkedin.com/in/ OR site:in.linkedin.com/pub/"

    # Output the query
    # print(query)

    return query