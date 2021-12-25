import json


class Config():
    def __init__(self,
        name                            = 'default_1',
        saliency_func_index             = 0,
        segmentation_func_index         = 0,
        segmentation_k                  = 100,
        segmentation_saliency_threshold = 50,
        paint1_func_index               = 0,
        paint1_func_parameter           = 7,
        paint2_func_index               = 1,
        paint2_func_parameter           = 30
    ):
        self.name                            = name
        self.saliency_func_index             = saliency_func_index
        self.segmentation_func_index         = segmentation_func_index
        self.segmentation_k                  = segmentation_k
        self.segmentation_saliency_threshold = segmentation_saliency_threshold
        self.paint1_func_index               = paint1_func_index
        self.paint1_func_parameter           = paint1_func_parameter
        self.paint2_func_index               = paint2_func_index
        self.paint2_func_parameter           = paint2_func_parameter

        self.config_dict = {
            'name'                            : self.name,
            'saliency_func_index'             : self.saliency_func_index,
            'segmentation_func_index'         : self.segmentation_func_index,
            'segmentation_k'                  : self.segmentation_k,
            'segmentation_saliency_threshold' : self.segmentation_saliency_threshold,
            'paint1_func_index'               : self.paint1_func_index,
            'paint1_func_parameter'           : self.paint2_func_index,
            'paint2_func_index'               : self.paint2_func_index,
            'paint2_func_parameter'           : self.paint2_func_parameter
        }


    def load_para_from_json(self, input_json_file_path):
        json_file = open(input_json_file_path, 'r')
        json_object = json.load(json_file)    
        return json_object


    def update_param(self, dict):
        self.name                            = dict['name']
        self.saliency_func_index             = dict['saliency_func_index']
        self.segmentation_func_index         = dict['segmentation_func_index']
        self.segmentation_k                  = dict['segmentation_k']
        self.segmentation_saliency_threshold = dict['segmentation_saliency_threshold']
        self.paint1_func_index               = dict['paint1_func_index']
        self.paint1_func_parameter           = dict['paint1_func_parameter']
        self.paint2_func_index               = dict['paint2_func_index']
        self.paint2_func_parameter           = dict['paint2_func_parameter']

        self.config_dict = {
            'name'                            : self.name,
            'saliency_func_index'             : self.saliency_func_index,
            'segmentation_func_index'         : self.segmentation_func_index,
            'segmentation_k'                  : self.segmentation_k,
            'segmentation_saliency_threshold' : self.segmentation_saliency_threshold,
            'paint1_func_index'               : self.paint1_func_index,
            'paint1_func_parameter'           : self.paint2_func_index,
            'paint2_func_index'               : self.paint2_func_index,
            'paint2_func_parameter'           : self.paint2_func_parameter
        }



