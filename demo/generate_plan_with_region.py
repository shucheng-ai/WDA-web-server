# coding:utf-8
# from layout import generate_plan_within_region
# from tools import renderer, analysis

room = {
    "bbox": [[0, 0], [50000, 80000]],
    "obstacles": [
        {
            "polygon": [[0, 0], [50000, 0], [50000, 80000], [0, 80000]],
            "type": "wall"
        },
        {
            "polygon": [[10000, 20000], [11000, 20500], [10000, 21000], [9000, 20500]],
            "type": "column"
        },
        {
            "polygon": [[25000, 40000], [26000, 40500], [25000, 41000], [24000, 40500]],
            "type": "column"
        },
        {
            "polygon": [[40000, 60000], [41000, 60500], [40000, 61000], [39000, 60500]],
            "type": "column"
        }
    ],
    "height": 6000,
    "info": "暂无"
}

region = [[0, 0], [30000, 40000]]

history = {
    "moving_path": [
        [[0, 30000], [75000, 33000]],
        [[25000, 0], [27000, 80000]]
    ],
    "obstacles": [
        [[0, 0], [10000, 10000]],
        [[40000, 70000], [50000, 80000]]
    ],
    # regions moving_path obstacles 均用矩阵列表去描述
    "plans": {
        "rack1": {
        },
        "rack2": {
        }
    }
}

base_rack = "single-apr"

params = {
    'test_apr': {
        'name': 'test_apr',
        'description': '测试apr独特参数',
        'value': 0
    },
    'test_choice': {
        'name': 'test_choice',
        'description': '测试选项参数',
        'value': 1,
        'choices': [1, 3, 1000]
    },
    'test_range': {
        'name': 'test_range',
        'description': '测试范围限制参数',
        'value': 1,
        'range': (1, 10)
    },
    'test_str': {
        'name': 'test_str',
        'description': '测试字符串参数',
        'value': 'money'
    }
}

info = {
    "quantity": 1000,
    "direction": "horizontal"
}

# plan = generate_plan_within_region(room, region, history, base_rack, params, info)
# print("plan : ", plan)
# print("render : ", renderer.render(plan))
# print("plan_info : ", analysis.plan_info(plan, params));
