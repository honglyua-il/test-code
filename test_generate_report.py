#!/usr/bin/env python3
# Test script to verify the generate_report function works with the new batch size format

def test_generate_report():
    # Sample data in the new format with batch size dimension
    all_results = [
        {
            'name': 'resnet50',
            'result': {
                'fp16': {
                    'status': 'PASS',
                    '1': {
                        'Acc1': 0.761,
                        'Acc5': 0.929,
                        'FPS': 626.034,
                        'Cost time (s)': 189.88193455990404,
                        'status': 'PASS'
                    },
                    '32': {
                        'Acc1': 0.762,
                        'Acc5': 0.929,
                        'FPS': 4396.595,
                        'Cost time (s)': 140.23704537306912,
                        'status': 'PASS'
                    },
                    '64': {
                        'Acc1': 0.762,
                        'Acc5': 0.929,
                        'FPS': 4644.895,
                        'Cost time (s)': 141.181786688976,
                        'status': 'PASS'
                    }
                },
                'int8': {
                    'status': 'PASS',
                    '1': {
                        'Acc1': 0.759,
                        'Acc5': 0.928,
                        'FPS': 901.991,
                        'Cost time (s)': 197.5754367900081,
                        'status': 'PASS'
                    },
                    '32': {
                        'Acc1': 0.759,
                        'Acc5': 0.928,
                        'FPS': 9400.185,
                        'Cost time (s)': 139.12636023689993,
                        'status': 'PASS'
                    },
                    '64': {
                        'Acc1': 0.759,
                        'Acc5': 0.928,
                        'FPS': 9975.731,
                        'Cost time (s)': 139.0801616020035,
                        'status': 'PASS'
                    }
                }
            },
            'status': 'PASS'
        },
        {
            'name': 'yolov5',
            'result': {
                'fp32': {
                    'status': 'PASS',
                    '1': {
                        'IoU=0.50:0.95': 0.374,
                        'IoU=0.50': 0.582,
                        'FPS': 45.2,
                        'Cost time (s)': 220.5,
                        'status': 'PASS'
                    },
                    '8': {
                        'IoU=0.50:0.95': 0.373,
                        'IoU=0.50': 0.581,
                        'FPS': 320.1,
                        'Cost time (s)': 25.1,
                        'status': 'PASS'
                    }
                }
            },
            'status': 'PASS'
        },
        {
            'name': 'failing_model',
            'result': {},
            'status': 'FAIL'
        }
    ]

    # Import and run the function
    from generate_report import generate_report
    generate_report(all_results)
    print("Test completed successfully!")

if __name__ == "__main__":
    test_generate_report()