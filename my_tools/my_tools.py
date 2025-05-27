import json

def convert_to_list(keyword_string):
        # Replace "and" with a comma for consistency
        keyword_string = keyword_string.replace("and", ",")
        # Split the string by commas, strip extra spaces, and filter out empty strings
        keywords = [pos.strip() for pos in keyword_string.split(",") if pos.strip()]
        print(keywords)
        return keywords

def keyword_creator(position, industry):
    
    convert_to_list(position)
    convert_to_list(industry)
    # Define the lists for positions and industries
    positions = ['Legal Head', 'VP', 'AVP', 'AGM', 'GM']
    industries = ['MSME', 'SME']

    # Generate the query
    position_query = " OR ".join(f'"{position}"' for position in positions)
    industry_query = " AND ".join(f'"{industry}"' for industry in industries)

    # Final search pattern
    search_query = (
        f"{position_query} {industry_query} -intitle:\"profiles\" -inurl:\"dir/ \" "
        "site:in.linkedin.com/in/ OR site:in.linkedin.com/pub/"
    )

    print("Generated Search Query:")
    print(search_query)
    return search_query

# positions = "Legal Head, VP, AVP, AGM, GM"
# industries = "MSME, SME"

# keyword_creator(positions, industries)