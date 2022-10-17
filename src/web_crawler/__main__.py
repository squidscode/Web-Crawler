import requests
import json
from bs4 import BeautifulSoup
import concurrent.futures
from . import functions
from . import global_variables

if __name__ == "__main__":
    global_variables.init()

    count = 0
    # with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=global_variables.data["MAX_WORKERS"])
    for URL_suffix in global_variables.data["URL_pages"]:
        # if URL_suffix != "A": 
        #     continue
        try:
            page = requests.get(global_variables.data["URL_start"] + URL_suffix)
        except:
            print(global_variables.data["URL_start"] + URL_suffix + " ERROR!!")
            continue
        soup = BeautifulSoup(page.content, "html.parser")
        a_list = soup.find_all("a", href=functions.href_link, title=functions.has_title)
        for a in a_list:
            # if count >= 10: break
            if functions.valid_a_tag(a):
                print("Opening " + a["href"], end="... ")
                try:
                    subpage = requests.get(global_variables.data["URL_base"] + a["href"])
                except:
                    print(global_variables.data["URL_base"] + a["href"] + " ERROR!!")
                    continue
                subpage_soup = BeautifulSoup(subpage.content, "html.parser")
                # executor.submit(extract_page_content, recursive_print_content(a), subpage_soup)
                functions.extract_page_content(functions.recursive_print_content(a), subpage_soup)
                print("... DONE")
                count += 1
    executor.shutdown(wait=True, cancel_futures=False)

    print(global_variables.data["word_dictionary"])
    print("# of TV Shows: " + str(count))
    
    # Writing to "./WIP/Web\ Scraping/Data/television_programs.json"
    with open(global_variables.data["output_file"], "w") as outfile:
        json.dump(global_variables.data["word_dictionary"], outfile)