def getAADataByTicketReport(ticketID, db):
    try:
        if ticketID:
            doc = db(db.ticket_report.ticket_id == ticketID).select().first()
            data = []
            if doc['aaData_page_1'] is not None:
                data += doc['aaData_page_1']
            if doc['aaData_page_2'] is not None:
                data += doc['aaData_page_2']
            if doc['aaData_page_3'] is not None:
                data += doc['aaData_page_3']
            if doc['aaData_page_4'] is not None:
                data += doc['aaData_page_4']
            if doc['aaData_page_5'] is not None:
                data += doc['aaData_page_5']
            if doc['aaData_page_6'] is not None:
                data += doc['aaData_page_6']
            if doc['aaData_page_7'] is not None:
                data += doc['aaData_page_7']
            if doc['aaData_page_8'] is not None:
                data += doc['aaData_page_8']
            if doc['aaData_page_9'] is not None:
                data += doc['aaData_page_9']
            if doc['aaData_page_10'] is not None:
                data += doc['aaData_page_10']
            if doc:
                rs = []
                count = 0
                for v in data:
                    count += 1
                    v[0] = str(count)
                    rs.append(v)
                return rs
            else:
                return []
    except Exception as ex:
        return []
