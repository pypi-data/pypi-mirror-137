# commit
from client import RestClient
task_type = [
    'organic',
    'related_searches',
    'people_also_ask',
    'top_stories',
    'knowledge_graph'
]

task_params = {
    'organic': ['url', 'description', 'extended_people_also_search'],
    # 'related_searches' : Not required
    'people_also_ask': ['title', 'title2', 'url', 'description'],
    # top_stories['items'] params
    'top_stories': ['domain', 'title', 'date', 'url'],
    'knowledge_graph': ['text', 'title', 'url', 'title']

}
# Request
client = RestClient('gpxfbhbgssdqcncbat@bvhrs.com', '239f87a1b59018ed')

def make_request(keyword, email='gpxfbhbgssdqcncbat@bvhrs.com', api_key='239f87a1b59018ed'):
    client = RestClient(email, api_key)
    post_data = dict()
    post_data[len(post_data)] = dict(
        language_name="English",
        location_name="United States",
        keyword=keyword,
        priority=2,
        depth=2,
        max_crawl_pages=2,
        tag=f"{keyword} google",
    )
    response = client.post(
        "/v3/serp/google/organic/task_post", post_data)
    if response["status_code"] == 20000:
        print('please wait for sometime.. till we gather data')
        return(response, response['tasks'][0]['id'])
    else:
        print("error. Code: %d Message: %s" %
              (response["status_code"], response["status_message"]))


def make_live_request(keyword, email='gpxfbhbgssdqcncbat@bvhrs.com', api_key='239f87a1b59018ed'):
    client = RestClient(email, api_key)
    post_data = dict()
    post_data[len(post_data)] = dict(
        language_name="English",
        location_name="United States",
        keyword=keyword,
        priority=2,
        depth=2,
        max_crawl_pages=2,
        tag=f"{keyword} google",
    )
    response = client.post(
        "/v3/serp/google/organic/live/advanced", post_data)
    if response["status_code"] == 20000:
        print('please wait for sometime.. till we gather data')
        return(response, response['tasks'][0]['id'])
    else:
        print("error. Code: %d Message: %s" %
              (response["status_code"], response["status_message"]))


def get_response(uuid, res_type):
    response = client.get(f"/v3/serp/google/organic/task_get/advanced/{uuid}")
    # print(response)
    if response['status_code'] == 20000:
        # results = []
        # for task in response['tasks']:
        #     if (task['result'] and (len(task['result']) > 0)):
        #         for resultTaskInfo in task['result']:
        #             if(resultTaskInfo[f'endpoint_{res_type}']):
        #                 results.append(client.get(
        #                     resultTaskInfo[f'endpoint_{res_type}']))
        return response
    else:
        print("error. Code: %d Message: %s" %
              (response["status_code"], response["status_message"]))


def get_results(results, tasks, task_params):
    df = {}
    for i, data in enumerate(results['tasks'][0]['result'][0]['items']):
        task = data['type']
        if task == 'organic' and task in tasks:
            # [url, description, extended_people_also_search]
            for key in data.keys():
                if key in task_params[f'{task}']:
                    df[f'{task}_{key}'] = str(data[f'{key}'])

        if task == 'people_also_ask' and task in tasks:
            all_items = {f'{task}_{param}': list()
                                                 for param in task_params[task]}
            for item in data['items']:
                all_items[f'{task}_title'].append(item[f'title'])
                for key in item['expanded_element'][0].keys():
                    if key in task_params[task]:
                        all_items[f'{task}_{key}'].append(
                            item['expanded_element'][0][f'{key}'])
            all_items = {k: str(v) for k, v in all_items.items()}
            df.update(all_items)

        if task == 'related_searches' and task in tasks:
            df[f'{task}_items'] = str(data[f'items'])

        # put top_stories['items'] params in task_params
        if task == 'top_stories' and task in tasks:
            # [domain, title, date, url]
            all_items = {f'{task}_{param}': list()
                                                 for param in task_params[task]}
            all_items[f'{task}_title'].append(data['title'])
            for item in data['items']:
                for key in item.keys():
                    if key in task_params[f'{task}'] and key != 'title':
                        all_items[f'{task}_{key}'].append(item[f'{key}'])
                    # df[f'{task}_{key}'] = data[f'{key}']
            all_items = {k: str(v) for k, v in all_items.items()}
            df.update(all_items)

        if task == 'knowledge_graph' and task in tasks:
            all_items = {f'{task}_{param}': list()
                                                 for param in task_params[task]}
            #[title, url, text]
            all_items.update({f'{task}_main_title': list(),
                             f'{task}_description': list()})
            all_items[f'{task}_main_title'].append(data[f'title'])
            all_items[f'{task}_description'].append(data[f'description'])
            for item in data['items']:

                   try:
                        all_items[f'{task}_text'].append(item[f'text'])
                    except:
                        all_items[f'{task}_text'].append(None)
                    for key in item.keys():
                        if key in task_params[f'{task}'] and key != 'text':
                            try:
                                all_items[f'{task}_{key}'].append(item['links'][0][f'{key}'])
                            except:
                                all_items[f'{task}_{key}'].append(None)
            all_items = {k: str(v) for k, v in all_items.items()}
            df.update(all_items)

    return df
