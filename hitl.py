import json, datetime
LOG='escalations.jsonl'
def escalate(query, draft):
    rec={'time':datetime.datetime.utcnow().isoformat(),'query':query,'draft':draft}
    with open(LOG,'a') as f: f.write(json.dumps(rec)+'\n')
    return 'Your request has been escalated to a human support agent.'
