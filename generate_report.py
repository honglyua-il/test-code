def generate_report(all_results):
    print(all_results)
    # 区分两种数据结构的键
    detection_keys = {"IoU=0.50:0.95", "IoU=0.50"}
    classification_keys = {"Top1 acc", "Top5 acc", "Acc1", "Acc5"}
    default_ret_keys = ['status', 'Cost time (s)']

    model_count=0
    fail_model=0
    fail_model_name = []
    for item in all_results:
        model_count +=1
        if item["status"] == "FAIL":
            fail_model +=1
            fail_model_name.append(item['name'])
    fail_model_info = "Fail Models: " + ",".join(fail_model_name)
    succ_model= model_count-fail_model

    # 生成 HTML 表格
    html_output = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>JSON to HTML Table</title>
        <style>
            table {
                width: 100%;
                border-collapse: collapse;
            }
            th, td {
                border: 1px solid black;
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
        </style>
    </head>
    <body>
    """
    html_sum = f"""
        <h1>Test Cases: {model_count}, Pass Cases: {succ_model}, Fail Cases: {fail_model}, {fail_model_info}</h1>
    """
    html_output += html_sum
    html_detec_body = """
        <h1>Detection Results</h1>
        <table border="1">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Precision</th>
                    <th>Batch Size</th>
                    <th>Status</th>
                    <th>Cost time (s)</th>
                    <th>IoU=0.50:0.95</th>
                    <th>IoU=0.50</th>
    """
    html_tbody = """
            </tbody>
        </table>
    """
    html_clf_body = """
        <h1>Classification Results</h1>
        <table border="1">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Precision</th>
                    <th>Batch Size</th>
                    <th>Status</th>
                    <th>Cost time (s)</th>
                    <th>Top1 acc</th>
                    <th>Top5 acc</th>
    """

    # 填充检测结果的表格
    for item in all_results:
        if item["status"] == "FAIL":
            html_output += f"""
                <h1>{item['name']} Results</h1>
                <table border="1">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Status</th>
                        </tr>
                     </thead>
                    <tbody>
                        <tr>
                            <td>{item['name']}</td>
                            <td style="color:red">{item['status']}</td>
                        </tr>
                    </tbody>
                </table>
            """
            continue

        html_other_body = f"""
        <h1>{item['name']} Results</h1>
        <table border="1">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Precision</th>
                    <th>Batch Size</th>
                    <th>Status</th>
                    <th>Cost time (s)</th>
    """
        html_detec_tr_content = ""
        html_clf_tr_content = ""
        html_other_tr_content = ""
        
        # Collect all possible keys from nested structure (precision -> batch_size -> metrics)
        all_nested_keys = set()
        for precision_name, precision_data in item['result'].items():
            # Check if precision_data has batch size structure
            for key, value in precision_data.items():
                if key not in ['status', 'Cost time (s)']:  # These are batch sizes like '1', '32', '64'
                    if isinstance(value, dict):  # This is a batch size entry
                        all_nested_keys.update(value.keys())
        
        new_th_row = list(all_nested_keys - set(default_ret_keys) - set(detection_keys) - set(classification_keys))
        th_row = ""
        if any(key in all_nested_keys for key in detection_keys):
            for retKey in new_th_row:
                th_row += f"<th>{retKey}</th>\n"
            html_detec_body += th_row + """</tr>
                </thead>
                <tbody>
            """
        elif any(key in all_nested_keys for key in classification_keys):
            for retKey in new_th_row:
                th_row += f"<th>{retKey}</th>\n"
            html_clf_body += th_row + """</tr>
                </thead>
                <tbody>
            """
        else:
            for retKey in new_th_row:
                th_row += f"<th>{retKey}</th>\n"
            html_other_body += th_row + """</tr>
                </thead>
                <tbody>
            """
        
        # Process each precision and its batch sizes
        for precision, precision_data in item['result'].items():
            # Extract the overall status for the precision level
            precision_status = precision_data.get('status', 'PASS')
            overall_cost_time = precision_data.get('Cost time (s)', 'N/A')
            
            # Process each batch size within the precision
            for batch_size, result in precision_data.items():
                if batch_size in ['status', 'Cost time (s)']:  # Skip these as they are not batch sizes
                    continue
                    
                if isinstance(result, dict):  # This is batch size data
                    td_status = f"""<td style="color:blue">{result.get('status', precision_status)}</td>"""
                    if result.get('status', precision_status) != "PASS":
                        td_status = f"""<td style="color:red">{result.get('status', precision_status)}</td>"""

                    row = f"""
                        <tr>
                            <td>{item['name']}</td>
                            <td>{precision}</td>
                            <td>{batch_size}</td>
                            {td_status}
                            <td>{result.get('Cost time (s)', 'N/A')}</td>
                    """
                    if any(key in result for key in detection_keys):
                        iou_95 = result.get('IoU=0.50:0.95', 'N/A')
                        iou_50 = result.get('IoU=0.50', 'N/A')
                        row += f"""        <td>{iou_95}</td>
                        <td>{iou_50}</td>
                        """
                        for retKey in new_th_row:
                            row += f"        <td>{result.get(retKey, 'N/A')}</td>\n"
                        html_detec_tr_content += row + "</tr>\n"
                    elif any(key in result for key in classification_keys):
                        top1_acc = result.get('Top1 acc', result.get('Acc1', 'N/A'))
                        top5_acc = result.get('Top5 acc', result.get('Acc5', 'N/A'))
                        row += f"""        <td>{top1_acc}</td>
                        <td>{top5_acc}</td>
                        """
                        for retKey in new_th_row:
                            row += f"        <td>{result.get(retKey, 'N/A')}</td>\n"
                        html_clf_tr_content += row + "</tr>\n"
                    else:
                        for retKey in new_th_row:
                            row += f"        <td>{result.get(retKey, 'N/A')}</td>\n"
                        html_other_tr_content += row + "</tr>\n"

        if html_detec_tr_content != "":
            html_output += html_detec_body.replace("Detection", item['name']) + html_detec_tr_content + html_tbody
            
        if html_clf_tr_content != "":
            html_output += html_clf_body.replace("Classification", item['name']) + html_clf_tr_content + html_tbody
        
        if html_other_tr_content != "":
            html_output += html_other_body + html_other_tr_content + html_tbody

    html_output += """
    </body>
    </html>
    """

    # 将HTML内容写入文件
    html_file_path = '/workspace/output.html'
    with open(html_file_path, 'w') as f:
        f.write(html_output)

    print(f"HTML file has been written to {html_file_path}")