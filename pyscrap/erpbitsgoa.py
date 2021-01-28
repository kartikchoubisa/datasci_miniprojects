from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import itertools as it
import pandas as pd
import re



website_link = "https://sis.erp.bits-pilani.ac.in/psp/sisprd/?cmd=login"

username = "31120190896"
password = "HIUE^5hD"


HELS = ['SYMBOLIC LOGIC',
        'PROFESSIONAL ETHICS',
        'INTRODUCTORY PHILOSOPHY',
        'MOD POLITICAL CONCEPTS',
        'LINGUISTICS',
        'Urban Modrn & Renewal of Paris',
        'Shakespeare and Popular Cultur',
        'Cities-Life Issues & Conflicts',
        'DISASTER AND DEVELOPMENT',
        'ENG LIT FORM AND MOV',
        'MAIN TRENDS IN IND HIST',
        'CROSS CULTURAL SKILLS',
        'INTERNATIONAL RELATIONS',
        'INTRO TO CARNATIC MUSIC',
        'ENVIRON DEV & CLIMATE CH',
        'CONTEMPORARY INDIA',
        'CRITI ANAL OF LIT & CINE',
        'EFFECTIVE PUBLIC SPEAK',
        'PUBLIC POLICY',
        'DYN OF SOCIAL CHANGE',
        'DEVELOPMENT ECONOMICS',
        'ECOCRITICISM',
        'BUSINESS COMMUNICATION',
        ]

DELS = ['THEORY OF RELATIVITY',
        'INTRO TO ASTRO & ASTROPH',
        ]

driver = webdriver.Chrome("chromedriver.exe")
driver.implicitly_wait(5) # otherwise code breaks unexpectedly sometimes
driver.get(website_link)


def login(username, password):
    try:
        username_element = driver.find_element_by_id("userid")
        username_element.send_keys(username)
        print("username entered")
    except Exception as e:
        print("something wrong while entering username")
        print(e)

    try:
        password_element = driver.find_element_by_id("pwd")
        password_element.send_keys(password)
        print("password entered")
    except Exception as e:
        print("something wrong while entering password")
        print(e)

    try:
        submit_element = driver.find_element_by_name("Submit")
        submit_element.click()
        print("submit button clicked")
    except Exception as e:
        print("something wrong while clicking submit button")
        print(e)


def switch_to_content():
    try:
        iframe = driver.find_element_by_id("ptifrmtgtframe")
        driver.switch_to.frame(iframe)
    except:
        print('could not switch to contents frame (probably already in that frame)')

def click_subject_row_wise(table_num, row_num):
    """
    :param table_num: starts from 0 for 1-1
    :param row_num: starts from 1 for first subject
    :return: None
    """
    switch_to_content()
    row_id = f"trSAA_ACRSE_VW${table_num}_row{row_num}"
    sub_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//*[@id=\"{row_id}\"]/td[2]/div/span/a"))
    )
    sub_element.click()
    print(f"clicked subject: '{sub_element.text}'", end=" -> ")


def click_subject_by_name(name):
    # switch_to_content()
    sub = driver.find_element_by_link_text(name)
    print(f"clicked subject: {sub.text}", end=" -> ")
    sub.click()

def subject_details():
    subject = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "DERIVED_CRSECAT_DESCR200"))
    ).text

    view_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "DERIVED_SAA_CRS_SSR_PB_GO"))
    )
    view_button.click()
    print("clicked 'view class sections'", end=" -> ")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "DERIVED_SAA_CRS_TERM_ALT"))
    )
    drop_down = Select(driver.find_element_by_id("DERIVED_SAA_CRS_TERM_ALT"))
    drop_down.select_by_visible_text("FIRST SEMESTER 2020-2021")
    print("Selected 'FIRST SEMESTER 2020-2021'", end=" -> ")

    show_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "DERIVED_SAA_CRS_SSR_PB_GO$97$"))
    )
    show_button.click()
    print("clicked 'show selections'", end=" -> ")

    def count_desc():

        count_desc = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "PSGRIDCOUNTER"))
        ).text

        r1 = re.compile("^\d+-(\d+) of (\d+)")
        r2 = re.compile("^\d of (\d)")
        m1 = r1.findall(count_desc)
        m2 = r2.findall(count_desc)
        # print(f"{m1=}, {m2=}")
        # print(count_desc)
        if m1:
            expandable = m1[0][0] != m1[0][1]
            entries_count = int(m1[0][1])
        elif m2:
            expandable = False
            entries_count = int(m2[0][0])
        else:
            print("NO MATCH")
        return expandable, entries_count

    expandable, entries_count = count_desc()

    if expandable:
        view_all_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "CLASS_TBL_VW5$fviewall$0"))
        )
        view_all_button.click()
        # print("clicked 'view all'")
        time.sleep(1) # gotta sleep after clicking view all
    # else:
    #     print("not expandable")

    # """
    # section tag a, id: CLASS_SECTION$0,
    # session tag span, id: CLASS_SESSION$0,
    # fn/an tag span, id: ZZZ_DERIVED_SR_DESCR_2$0,
    # exam date tag span, id: ZZZ_DERIVED_SR_EXAM_DT$0,
    # days tag span, id: MTGPAT_DAYS$0,
    # start tag span, id: MTGPAT_START$0,
    # end tag span, id: MTGPAT_END$0,
    # room tag span, id: MTGPAT_ROOM$0,
    # instructor tag span, id: MTGPAT_INSTR$0
    # """

    for i in range(entries_count):
        details_dict = {}

        details_dict['Subject'] = subject
        details_dict['Section'] = driver.find_element_by_id(f'CLASS_SECTION${i}').text
        details_dict['Session'] = driver.find_element_by_id(f'CLASS_SESSION${i}').text
        details_dict['FN/AN'] = driver.find_element_by_id(f'ZZZ_DERIVED_SR_DESCR_2${i}').text  # this is broken
        details_dict['Exam Date'] = driver.find_element_by_id(f'ZZZ_DERIVED_SR_EXAM_DT${i}').text
        details_dict['Days'] = driver.find_element_by_id(f'MTGPAT_DAYS${i}').text
        details_dict['Start'] = driver.find_element_by_id(f'MTGPAT_START${i}').text
        details_dict['End'] = driver.find_element_by_id(f'MTGPAT_END${i}').text
        details_dict['Room'] = driver.find_element_by_id(f'MTGPAT_ROOM${i}').text
        details_dict['Instructor'] = driver.find_element_by_id(f'MTGPAT_INSTR${i}').text
        yield details_dict
    assert i == entries_count-1
    print(f"collected {entries_count} entries", end="\n\n")  # note that i starts from 0

def view_all_electives(electives_type):
    switch_to_content()
    if electives_type == 'hel':
        id_num = 9
    elif electives_type == 'del':
        id_num = 12
    else:
        print("ELECTIVES ID BROKEN")
        return
    view_all_electives_button = driver.find_element_by_id(f"SAA_ACRSE_VW$fviewall${id_num}")
    if view_all_electives_button.text == "View All":
        view_all_electives_button.click()
        print(f"clicked 'view all' ({electives_type}) button", end=" -> ")
        time.sleep(1) # gotta sleep after clicking viewall!!!

    else:
        print(f"'view all' ({electives_type}) already expanded", end=" -> ")
        switch_to_content() # if not clicked then switch back to our frame

def get_CDCs():
    for row_num in it.count(1):
        try:
            click_subject_row_wise(2, row_num)
        except:
            print(f"collected data for {row_num - 1} subjects")
            break

        for details_dict in subject_details():  # yields dicts containing info about each class/lec/tut
            details_dict['Type'] = 'CDC'
            print(details_dict)
            data.append(details_dict)

        driver.back()
        driver.switch_to.default_content()

def get_electives(subjects_list: list, electives_type: str):
    """

    :param subjects_list:
    :param electives_type: 'hel' or 'del'
    :return:
    """

    for i, subject in enumerate(subjects_list, 1):
        print(f"{electives_type} {i}/{len(subjects_list)}", end=": ")
        view_all_electives(electives_type=electives_type)
        click_subject_by_name(subject)
        try:
            for details_dict in subject_details():
                details_dict['Type'] = electives_type.upper()
                data.append(details_dict)
                print(details_dict)

            driver.back()

        except Exception as e:
            corrupt_subjects.append(subject)
            print(f"couldn't extract data for {subject}")
            print(e)

def write_data():
    df = pd.DataFrame(data)
    df.to_csv('erpbitsgoa_mycourses -- new.csv')
    print("csv exported")

def verify():
    csv_old = pd.read_csv('erpbitsgoa_mycourses.csv')
    csv_new = pd.read_csv('erpbitsgoa_mycourses -- new.csv')

    print(f"{csv_old.equals(csv_new)=}")


login(username, password)
time.sleep(2)
driver.find_element_by_link_text("Self Service").click()
time.sleep(2)
driver.find_element_by_link_text("Degree Progress/Graduation").click()
time.sleep(2)
driver.find_element_by_link_text("My Academic Requirements").click()
print("Reached 'My Academic Requirements'")

data = []
corrupt_subjects = []  # some hels are not extracted sometimes, idk why (only sometimes)


get_CDCs() # get data for each of the compulsary subjects in 2-1

time.sleep(3)
get_electives(HELS, 'hel')
time.sleep(3)
get_electives(DELS, 'del')
print(f"{corrupt_subjects=}")

write_data() # make csv and dataframe
verify() # verify no change

# click_subject_row_wise(2,2)
# for i in subject_details():
#     print(i)


"""

trSAA_ACRSE_VW$0_row1
trSAA_ACRSE_VW$1_row1

//*[@id="trSAA_ACRSE_VW$6_row1"]/td[1]
//*[@id="CRSE_DESCR$28"]
//*[@id="CRSE_DESCR$15"]
//*[@id="CRSE_DESCR$16"]

//*[@id="trSAA_ACRSE_VW$2_row2"]/td[2]/div/span/a

{section, id: CLASS_SECTION$0,
session tag span, id: CLASS_SESSION$0,
fn/an tag span, id: ZZZ_DERIVED_SR_DESCR_2$0,
exam date tag span, id: ZZZ_DERIVED_SR_EXAM_DT$0,
days tag span, id: MTGPAT_DAYS$0,
start tag span, id: MTGPAT_START$0,
end tag span, id: MTGPAT_END$0,
room tag span, id: MTGPAT_ROOM$0,
instructor tag span, id: MTGPAT_INSTR$0}

"""
