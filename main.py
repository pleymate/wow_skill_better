from selenium import webdriver
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

def find_duplicate(list, element):
    for i in range(len(list)):
        if list[i][0] == element:
            return True
    return False

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--log-level=3')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    print("Starting Chrome driver")
    driver = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Driver\chromedriver.exe', chrome_options=options)
    return driver

def get_url(driver):
    list_class = [["warrior", 1], ["paladin", 2], ["hunter", 3], ["rogue", 4], ["priest", 5], ["death knight", 6], ["shaman", 7], ["mage", 8], ["warlock", 9], ["monk", 10], ["druid", 11], ["demon hunter", 12]]
    print("Classes: " + str(list_class))
    input_class = input("Enter class (case sensitive): ")
    for i in range(len(list_class)):
        if list_class[i][0] == input_class:
            id = list_class[i][1]
            break
        if i == len(list_class) - 1:
            print("Class not found")
    input_game = input("Enter game (wotlk, tbc): ")
    driver.get("https://wotlkdb.com/?locale=0")
    if input_game == "wotlk":
        url = "https://wotlkdb.com/?spells=7." + str(id)
    elif input_game == "tbc":
        url = "https://tbcdb.com/?spells=7." + str(id)
    return url

def get_max_elements(driver, url):
    driver.get(url)
    page_details_element = driver.find_elements_by_class_name("listview-nav")[0].find_elements_by_tag_name("span")
    page_details_string = ""
    for i in range(len(page_details_element)):
        page_details_string += page_details_element[i].text
    page_details_string = page_details_string.split("of ")[1]
    return int(page_details_string)

def get_spell_list(driver, max_elements, url):
    index = 0
    list = []
    while index < max_elements:
        driver.get(url + "#" + str(index) + "+1+13+3")
        driver.get(url + "#" + str(index) + "+1+13+3")#dont ask me why
        if "tbc" in url:
            table = driver.find_elements_by_class_name("listview-std")[0]
        if "wotlk" in url:
            table = driver.find_elements_by_class_name("listview-mode-default")[0]
        tr_elements = table.find_elements_by_tag_name("tr")
        for i in range(len(tr_elements)):
            td_elements = tr_elements[i].find_elements_by_tag_name("td")
            if i > 0:
                skill_name = td_elements[1].find_elements_by_tag_name("a")[0].text
                if "Passive" in skill_name:
                    continue
                skill_name_rank = td_elements[1].find_elements_by_tag_name("div")[0].text
                buffer = filter(str.isdigit, skill_name_rank)
                skill_rank = "".join(buffer)
                if not find_duplicate(list, skill_name) and (skill_rank == "" or skill_rank == "1"):
                    skill_href = td_elements[1].find_elements_by_tag_name("a")[0].get_attribute("href")
                    skill_id = skill_href.split("=")[1]
                    print(skill_name)
                    list.append([skill_name, skill_id])
        index += 50
    return list

def print_results(list):
    for i in range(len(list)):
        print('private string ' + ''.join(e for e in list[i][0] if e.isalnum() or e == " ").replace(" ", "") + ' = "' + list[i][0] + '";')
    print("\n")
    for i in range(len(list)):
        print('AddSpell(' + ''.join(e for e in list[i][0] if e.isalnum() or e == " ").replace(" ", "") + ', ' + list[i][1] + ', "None");')

driver = get_driver()
url = get_url(driver)
max_elements = get_max_elements(driver, url)
spell_list = get_spell_list(driver, max_elements, url)
print_results(spell_list)
driver.quit()

#todo add specs choice