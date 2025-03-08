import json 
from copy import deepcopy


def get_clean_ann_data(data_ann_file):
        
        """
        Get clean annotation data: Removes class 0 that is added by default to Roboflow datasets and shifts annotation ids by 1
        """
        data_ann = json.load(open(data_ann_file, 'r'))
        new_data_ann = {}
        if data_ann['info']:
            new_data_ann['info'] = data_ann['info']
        if data_ann['licenses']:
            new_data_ann['licenses'] = data_ann['licenses']

        # confirm if category 0 is none
        assert(data_ann['categories'][0]['supercategory']=='none'), "Need to change logic for removing category 0 from dataset in preprocessing"

        # data_ann['categories'] = [cat for cat in data_ann['categories'] if cat['id']!=0]
        new_data_ann['categories'] = [{'id': cat['id']-1, 'name': cat['name'], 'supercategory': cat['supercategory']} for cat in data_ann['categories'] if cat['id']!=0]

        new_data_ann['images'] = data_ann['images']
        new_data_ann['annotations'] = deepcopy(data_ann['annotations'])

        for ann in new_data_ann['annotations']:
            ann['category_id'] = ann['category_id']-1

        ID2CLASS = {}
        for cat_info in new_data_ann['categories']:
            ID2CLASS[cat_info['id']] = cat_info['name']

        return new_data_ann, ID2CLASS

def get_rf_cat_info(anno_data):

    categories = anno_data['categories']
    category_list = deepcopy(categories)
    image_count = {x['id']: set() for x in category_list}
    ann_count = {x['id']: 0 for x in category_list}
    
    for x in anno_data['annotations']:
        image_count[x['category_id']].add(x['image_id'])
        ann_count[x['category_id']] += 1
    
    for x in category_list:
        x['image_count'] = len(image_count[x['id']])
        x['instance_count'] = [x['id']]
    return categories, category_list