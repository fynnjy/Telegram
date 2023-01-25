import ytParser
import json


def json_database_creation():
    '''Creating a JSON DataBase when the bot starts'''
    new_dict = {'Values': [{'user_id': []}]}

    with open('Dicts/users.json', 'w', encoding='utf-8') as file:
        json.dump(new_dict, file, indent=4, ensure_ascii=False)


def smart_user_json_creation():
    '''Creating a JSON DataBase when the bot starts'''
    new_dict = {'Values': [{f'{user_id}': [{"Instagram": []}, {"YouTube": []}, {"TikTok": []}]}]}

    with open('new_dict.json', 'w', encoding='utf-8') as file:
        json.dump(new_dict, file, indent=4, ensure_ascii=False)


def new_bot_user(user_id):
    '''Creating a new user in the users file'''
    with open('Dicts/users.json', 'r', encoding='utf-8') as file:
        check_data = json.load(file)

    users_list = []
    for users in check_data['Values']:
        for k, v in users.items():
            users_list.append(k)

    if str(user_id) not in users_list:
        new_user = {f'{user_id}': [{"Instagram": []}, {"YouTube": []}, {"TikTok": []}]}

        with open('Dicts/users.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            data['Values'].append(new_user)

        with open('Dicts/users.json', 'w', encoding='utf-8') as new:
            json.dump(data, new, indent=4, ensure_ascii=False)

        user_status = {
            'status': 'new'
        }

        with open('Dicts/existinguser.json', 'w', encoding='utf-8') as file:
            json.dump(user_status, file, indent=4, ensure_ascii=False)

    else:
        check_data['Values'].pop(users_list.index(str(user_id)))

        with open('Dicts/users.json', 'w', encoding='utf-8') as file:
            json.dump(check_data, file, indent=4, ensure_ascii=False)

        new_user = {f'{user_id}': [{"Instagram": []}, {"YouTube": []}, {"TikTok": []}]}

        with open('Dicts/users.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            data['Values'].append(new_user)

        with open('Dicts/users.json', 'w', encoding='utf-8') as new:
            json.dump(data, new, indent=4, ensure_ascii=False)

        user_status = {
            'status': 'old'
        }

        with open('Dicts/existinguser.json', 'w', encoding='utf-8') as file:
            json.dump(user_status, file, indent=4, ensure_ascii=False)


def network_choice(network):
    '''Tracking the social network you use'''
    relevant_network = {
        'relevant_network': network
    }

    with open('Dicts/relevant_network.json', 'w', encoding='utf-8') as file:
        json.dump(relevant_network, file, indent=4, ensure_ascii=False)


def keyboard_choice(keyboard):
    '''Tracking the social keyboard you use'''
    relevant_keyboard = {
        'relevant_keyboard': keyboard
    }

    with open('Dicts/relevant_keyboard.json', 'w', encoding='utf-8') as file:
        json.dump(relevant_keyboard, file, indent=4, ensure_ascii=False)


def create_yt_user(link, user_id):
    '''Creating a new user after inspections for YouTube'''
    with open('Dicts/users.json', 'r', encoding='utf-8') as file:
        check_data = json.load(file)

    if 'https://www.youtube.com/' in link or 'http://www.youtube.com/' in link\
            or 'https://youtube.com/' in link or 'http://youtube.com/' in link:
        new_id = link.split("/")[-1]

        users_list = []
        for users in check_data['Values']:
            for k, v in users.items():
                users_list.append(k)

        current_user = users_list.index(str(user_id))
        dict_of_current_user = check_data['Values'][current_user]

        social_networks_list = []
        for k, v in dict_of_current_user.items():
            for item in v:
                social_networks_list.append(item)

        instagram_dict = social_networks_list[0]
        youtube_dict = social_networks_list[1]
        tiktok_dict = social_networks_list[2]

        id_list = []
        for k, v in youtube_dict.items():
            for channels_id in v:
                id_list.append(channels_id['id'])

        if new_id in id_list:
            status = {
                'status': 'Oops. Such a user already exists 🚫'
            }

            with open('Dicts/user_status.json', 'w', encoding='utf-8') as file:
                json.dump(status, file, indent=4, ensure_ascii=False)

        elif new_id not in id_list:
            if ytParser.get_youtube_info(link) == 'non-existent':

                status = {
                    'status': 'Non-existent user ❌'
                }

                with open('Dicts/user_status.json', 'w', encoding='utf-8') as file:
                    json.dump(status, file, indent=4, ensure_ascii=False)

            else:
                name = link.split("/")[-1].title()
                subscribers_count = ytParser.get_youtube_info(link)

                yt_channels = []
                for k, v in youtube_dict.items():
                    for item in v:
                        yt_channels.append(item)

                new_user = {
                    'name': name,
                    'link': link,
                    'subscribers': subscribers_count,
                    'id': link.split("/")[-1]
                }

                yt_channels.append(new_user)

                youtube_dict = {'YouTube': yt_channels}

                social_networks = [instagram_dict, youtube_dict, tiktok_dict]

                check_data['Values'].pop(current_user)

                with open('Dicts/users.json', 'w', encoding='utf-8') as file:
                    json.dump(check_data, file, indent=4, ensure_ascii=False)

                new_user = {f'{user_id}': social_networks}

                with open('Dicts/users.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    data['Values'].append(new_user)

                with open('Dicts/users.json', 'w', encoding='utf-8') as new:
                    json.dump(data, new, indent=4, ensure_ascii=False)

                status = {
                    'status': 'User successfully added ✅'
                }

                with open('Dicts/user_status.json', 'w', encoding='utf-8') as file:
                    json.dump(status, file, indent=4, ensure_ascii=False)

    else:
        status = {
            'status': 'Incorrect link ❌'
        }

        with open('Dicts/user_status.json', 'w', encoding='utf-8') as file:
            json.dump(status, file, indent=4, ensure_ascii=False)


def delete_yt_user(link, user_id):
    '''Deleting a user if he is in the list'''
    with open('Dicts/users.json', 'r', encoding='utf-8') as file:
        check_data = json.load(file)

    if 'https://www.youtube.com/' in link or 'http://www.youtube.com/' in link\
            or 'https://youtube.com/' in link or 'http://youtube.com/' in link:
        users_list = []
        for users in check_data['Values']:
            for k, v in users.items():
                users_list.append(k)

        current_user = users_list.index(str(user_id))
        dict_of_current_user = check_data['Values'][current_user]

        social_networks_list = []
        for k, v in dict_of_current_user.items():
            for item in v:
                social_networks_list.append(item)

        instagram_dict = social_networks_list[0]
        youtube_dict = social_networks_list[1]
        tiktok_dict = social_networks_list[2]

        updated_list = []
        counter = False
        pop_id = link.split("/")[-1]
        for k, v in youtube_dict.items():
            for channel_id in v:
                if channel_id['id'] == pop_id:
                    counter = True
                    pass
                else:
                    updated_list.append(channel_id)

        youtube_dict = {'YouTube': updated_list}

        social_networks = [instagram_dict, youtube_dict, tiktok_dict]

        check_data['Values'].pop(current_user)

        with open('Dicts/users.json', 'w', encoding='utf-8') as file:
            json.dump(check_data, file, indent=4, ensure_ascii=False)

        new_user = {f'{user_id}': social_networks}

        with open('Dicts/users.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            data['Values'].append(new_user)

        with open('Dicts/users.json', 'w', encoding='utf-8') as new:
            json.dump(data, new, indent=4, ensure_ascii=False)

        if counter == True:
            status = {
                'status': 'User successfully deleted ✅'
            }

            with open('Dicts/user_status.json', 'w', encoding='utf-8') as file:
                json.dump(status, file, indent=4, ensure_ascii=False)

        else:
            status = {
                'status': 'This user was not on the list 🚫'
            }

            with open('Dicts/user_status.json', 'w', encoding='utf-8') as file:
                json.dump(status, file, indent=4, ensure_ascii=False)

    else:
        status = {
            'status': 'Incorrect link ❌'
        }

        with open('Dicts/user_status.json', 'w', encoding='utf-8') as file:
            json.dump(status, file, indent=4, ensure_ascii=False)


def get_info_update_yt(user_id):
    '''Data update. Collecting links, deletion and new link parsing'''
    with open('Dicts/users.json', 'r', encoding='utf-8') as file:
        check_data = json.load(file)

    users_list = []
    for users in check_data['Values']:
        for k, v in users.items():
            users_list.append(k)

    current_user = users_list.index(str(user_id))
    dict_of_current_user = check_data['Values'][current_user]

    social_networks_list = []
    for k, v in dict_of_current_user.items():
        for item in v:
            social_networks_list.append(item)

    instagram_dict = social_networks_list[0]
    youtube_dict = social_networks_list[1]
    tiktok_dict = social_networks_list[2]

    links = []
    for k, v in youtube_dict.items():
        for link in v:
            links.append(link['link'])

    if len(links) >= 1:
        check_data['Values'].pop(current_user)

        with open('Dicts/users.json', 'w', encoding='utf-8') as file:
            json.dump(check_data, file, indent=4, ensure_ascii=False)

        new_user = {f'{user_id}': [{"Instagram": []}, {"YouTube": []}, {"TikTok": []}]}

        with open('Dicts/users.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            data['Values'].append(new_user)

        with open('Dicts/users.json', 'w', encoding='utf-8') as new:
            json.dump(data, new, indent=4, ensure_ascii=False)

        for link in links:
            create_yt_user(link, user_id)

    else:
        return False


def youtube_list_deleting(user_id):
    '''Function that removes the entire YouTube list'''
    with open('Dicts/users.json', 'r', encoding='utf-8') as file:
        check_data = json.load(file)

    users_list = []
    for users in check_data['Values']:
        for k, v in users.items():
            users_list.append(k)

    current_user = users_list.index(str(user_id))
    current_dict = check_data['Values'][current_user]

    check_data['Values'].pop(current_user)

    with open('Dicts/users.json', 'w', encoding='utf-8') as file:
        json.dump(check_data, file, indent=4, ensure_ascii=False)

    new_user = {f'{user_id}': [{"Instagram": []}, {"YouTube": []}, {"TikTok": []}]}

    with open('Dicts/users.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        data['Values'].append(new_user)

    with open('Dicts/users.json', 'w', encoding='utf-8') as new:
        json.dump(data, new, indent=4, ensure_ascii=False)


# choose = int(input('Select an action: '
#                    '\n1) Add user'
#                    '\n2) Delete a user'
#                    '\n3) Update info'
#                    '\n\nSelection: '))
#
# if choose == 1:
#     link = input('Link: ')
#     create_user(link)
# elif choose == 2:
#     link = input('Link: ')
#     delete_user(link)
# elif choose == 3:
#     get_info_update()
# else:
#     print('Incorrect answer!')


