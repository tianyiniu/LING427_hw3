# P(suffixing | SOV) 
# There are much faster and more efficient ways to calculate this...

def format_joint_dict(joint_probs):
    for conditional_var in joint_probs:
        print(conditional_var)
        for resulting_var in joint_probs[conditional_var]:
            print(f"\t{resulting_var} : {joint_probs[conditional_var][resulting_var]}")

def calculate_affix_given_wordorder(tups):
    """Input tups: [(code, affix, word order), ...]"""
    # Tabulate joint counts
    joint_counts = {}
    for code, affix, word_order in tups:
        if word_order in joint_counts:
            if affix in joint_counts[word_order]: 
                joint_counts[word_order][affix] += 1
            else: 
                joint_counts[word_order][affix] = 1
        else: 
            joint_counts[word_order]= {affix: 1}
        
    # Calculate priors
    priors = {}
    for word_order in joint_counts:
        priors[word_order] = round(sum(list(joint_counts[word_order].values())) / len(tups), 3)
    print(priors)

    # Convert joint_counts into joint probabilities
    for word_order in joint_counts:
        word_order_counts = sum(list(joint_counts[word_order].values()))
        for affix in joint_counts[word_order]:
            joint_counts[word_order][affix] = round(joint_counts[word_order][affix] / word_order_counts, 3)
    return joint_counts

tups = [(row.wals_code, row.description_26A, row.description_81A) for row in df_merged.itertuples()]
affix_given_wordorder = calculate_affix_given_wordorder(tups)
format_joint_dict(affix_given_wordorder)

def calculate_wordorder_given_affix(tups):
    """Input tups: [(code, affix, word order), ...]"""
    # Tabulate joint counts
    joint_counts = {}
    for code, affix, word_order in tups:
        if affix in joint_counts:
            if word_order in joint_counts[affix]: 
                joint_counts[affix][word_order] += 1
            else: 
                joint_counts[affix][word_order] = 1
        else: 
            joint_counts[affix]= {word_order: 1}
    
    # Calculate priors
    priors = {}
    for affix in joint_counts:
        priors[affix] = round(sum(list(joint_counts[affix].values())) / len(tups), 3)
    print(priors)

    # Convert joint_counts into joint probabilities
    for affix in joint_counts:
        affix_counts = sum(list(joint_counts[affix].values()))
        for word_order in joint_counts[affix]:
            joint_counts[affix][word_order] = round(joint_counts[affix][word_order] / affix_counts, 3)
    return joint_counts

print("\n")
wordorder_given_affix = calculate_wordorder_given_affix(tups)
format_joint_dict(wordorder_given_affix)

# Calculate joint probabilities per language family

def format_prob_wordorder_and_affix(tups, family_name, probs_threshold=0.0):
    """Input tups: [(code, affix, word order), ...]"""
    # Tabulate joint counts
    joint_counts = {}
    for code, affix, word_order in tups:
        if affix in joint_counts:
            if word_order in joint_counts[affix]: 
                joint_counts[affix][word_order] += 1
            else: 
                joint_counts[affix][word_order] = 1
        else: 
            joint_counts[affix]= {word_order: 1}
    
    # Calculate priors
    priors = {}
    for affix in joint_counts:
        priors[affix] = round(sum(list(joint_counts[affix].values())) / len(tups), 3)

    # Convert joint_counts into joint probabilities
    for affix in joint_counts:
        for word_order in joint_counts[affix]:
            joint_counts[affix][word_order] = round(joint_counts[affix][word_order] / family_counts_dict[family_name], 3)

    # Format joint_counts for writing into output file
    lines = []
    for affix in joint_counts:
        lines.append("\t"+affix+"\n")
        for word_count_probs in joint_counts[affix]:
            if joint_counts[affix][word_count_probs] >= probs_threshold:
                lines.append(f"\t\t{word_count_probs} : {joint_counts[affix][word_count_probs]}\n")
            else: 
                continue

    return lines + ["\n"]
    
lines = []
for family_name, family_count in interested_families:
    lines += [f"{family_name}: {family_count} langauges\n"]
    family_dict = lang_families[family_name]
    # Format into list of tuples [(code, affix, word order)]
    tups = []
    for combination in family_dict:
        affix, word_order = combination
        codes = family_dict[combination]
        for wals_code in codes: 
            tups.append((wals_code, affix, word_order))
    lines += format_prob_wordorder_and_affix(tups, family_name, probs_threshold=0.0)

with open("joint_statistics_per_family.txt", "w", encoding="utf-8") as f: 
    f.writelines(lines)