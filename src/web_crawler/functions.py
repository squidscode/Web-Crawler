import re
from . import __main__
from . import global_variables

def recursive_print_content(content):
    ans_string = ''
    for item_of_content in content:
        if isinstance(item_of_content, str):
            ans_string += item_of_content
        else:
            ans_string += recursive_print_content(item_of_content)
    return ans_string

def href_link(href):
    return href and re.compile(global_variables.data["valid_re"]).search(href) and not re.compile(global_variables.data["invalid_re"]).search(href)

def has_title(title):
    return title

def valid_a_tag(tag):
    return len(tag.contents) > 0 and isinstance(tag.contents[0], str) and global_variables.data["invalid_contents"].count(tag.contents[0]) == 0

def no_class(class_):
    return not class_

def decode_words(series, p):
    para = recursive_print_content(p).split(" ")
    word_count = 0
    for word in para:
        word = re.sub(r"[,.!?(\[.*?\])(\n)(\")]", "", word.lower())
        if (len(word) <= 2 or word in global_variables.data["ignore_words"]): continue
        if word in global_variables.data["word_dictionary"]["word_map"] and word:
            if series in global_variables.data["word_dictionary"]["word_map"][word]:
                global_variables.data["word_dictionary"]["word_map"][word][series] = global_variables.data["word_dictionary"]["word_map"][word][series] + 1
            else:
                global_variables.data["word_dictionary"]["word_map"][word][series] = 1
        else:
            global_variables.data["word_dictionary"]["word_map"][word] = {}
            global_variables.data["word_dictionary"]["word_map"][word][series] = 1
        word_count += 1
    if series in global_variables.data["word_dictionary"]["series_count"]:
        global_variables.data["word_dictionary"]["series_count"][series] = global_variables.data["word_dictionary"]["series_count"][series] + word_count
    else:
        global_variables.data["word_dictionary"]["series_count"][series] = word_count
    

def target_section(series, soup, target_id, tag_budget, p_budget):
    target_span = soup.find("span", id=target_id)
    if target_span == None: 
        return (p_budget, {})
    target_h2 = target_span.parent
    seen_ps = set()
    print("HIT " + target_id + "!", end=" ")
    target_tag = target_h2.find_next_sibling()
    while tag_budget > 0 and p_budget > 0 and target_tag != None and target_tag.name != "h2":
        if target_tag.name == "p":
            decode_words(series, target_tag)
            seen_ps.add(target_tag) # add to seen_ps
            p_budget -= 1
        target_tag = target_tag.find_next_sibling()
        tag_budget -= 1
    return (p_budget, seen_ps)

# Plot -> Premise -> Synopsis -> Overview -> Episodes
def extract_page_content(series, soup):
    p_budget = global_variables.data["P_BUDGET"]
    seen_ps = set()
    for target_id in global_variables.data["target_ids"]:
        if p_budget == 0: break
        (p_budget, found_ps) = target_section(series, soup, target_id, global_variables.data["TAG_BUDGET"], p_budget)
        seen_ps = seen_ps.union(found_ps)
    if p_budget > 0:
        paras = soup.find_all("p", class_=no_class)
        for para in paras:
            if (p_budget == 0 or para in seen_ps): continue
            decode_words(series, para)
            p_budget -= 1