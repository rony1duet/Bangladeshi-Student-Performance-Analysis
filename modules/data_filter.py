from modules.utils import get_user_choice

def filter_data(data):
    location_choices = ["Urban", "Rural", "City", "All"]
    gender_choices = ["Male", "Female", "All"]
    group_choices = ["Science", "Commerce", "Humanities", "All"]
    location_choice = get_user_choice("Select Location:", location_choices)

    if location_choice != "All":
        data = data[data['location'] == location_choice]
    gender_choice = get_user_choice("Select Gender:", gender_choices)

    if gender_choice != "All":
        data = data[data['gender'] == gender_choice]
    group_choice = get_user_choice("Select Group:", group_choices)
    
    if group_choice != "All":
        data = data[data['stu_group'] == group_choice]
    return data

def filter_by_internet_access(data):
    internet_choices = ["Yes", "No", "All"]
    access_choice = get_user_choice("Select Internet Access:", internet_choices)
    if access_choice != "All":
        data = data[data['internet_access'] == access_choice]
    return data
