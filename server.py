"""
This is a simple Python Flask server with three rest 
endpoints to process the transactions of a given User account based on the constraints below.

Constraints:
- Oldest points to be spent first
- No payer's points should be negative

Returns:
    [Response]: Returns response with respective status codes
"""
from flask import Flask, request, jsonify
from datetime import datetime
from collections import deque

#Initiating the server
app = Flask("points_server")

#Global variables
#Dictionary to maintain points for a given payer
accounts = {}
total_points = 0

#Initializing a Queue to keep track of the incoming transactions
transactions = deque()
status_code = 200
content_header = {}
content_header["Content-type"] = "application/json"

def convert_date_to_datetime(date):
    """
    Function to convert Date object to Datetime object for better usability

    Args:
        date (Date): Date object in the given format (For example: 10/31 10AM)

    Returns:
        [DateTime]: Returns Datetime object
    """
    date = date+'2020'
    datetime_object = datetime.strptime(date, '%d/%j  %I%p%Y')
    return datetime_object

@app.route('/add_points',methods = ['POST'])
def add_points():
    """
    This is a REST endpoint to add points to the User account

    Returns:
        (Response Message,status code): Returns a success status code if request succeeded,
        else returns bad request by client error  
    """
    global total_points
    global status_code

    data = request.get_json(force=True)
    print(data)
    payer = str(data["payerName"])
    points = int(data["points"])
    datetime = str(data["transactionDate"])
    datetime = convert_date_to_datetime(datetime)

    '''
    When the points are positive, simply append the transaction to the queue
    When the points are negative, there are three conditions
    - when the payer already exists and deducting the incoming transactional points results in negative points value
    - when the payer already exists and deducting the incoming transactional points result in positive points value
    - when the first transactional points value is negative
    '''
    if points > 0:
        total_points+= points
        transactions.appendleft([payer,points,datetime])
        if payer not in accounts:
            accounts[payer] = points
        else:
            accounts[payer]+= points

    elif points < 0:
        if payer in accounts and (accounts[payer] - points) < 0:
            status_code =  400
            return ("Invalid transaction record",int(status_code),content_header)
        elif payer in accounts and (accounts[payer] - points) > 0:
            accounts[payer]+=points 
            total_points += points
            for i in range(len(transactions)-1,-1,-1):
                if transactions[i][0] == payer:
                    remaining = transactions[i][1] + points
                    if remaining <= 0:
                        del transactions[i]
                        points = remaining
                    else:
                        transactions[i][1] = remaining
                        break
        else:
            status_code = 400
            return ("Invalid transaction record",int(status_code),content_header)

    return("Points Added Successfully!",int(status_code),content_header)

@app.route('/delete_points',methods=['DELETE'])
def delete_points():
    """
    This is a REST endpoint to deduct points from the User account

    Returns:
        (JSON object): Returns a JSON object list of [payer, points deducted] after 
        deducting points from the user account 
        using the constraints
    """
    global total_points
    global status_code

    data = request.get_json(force=True)
    points_to_deduct = int(data["points_to_deduct"])
    if total_points < points_to_deduct:
        status_code = 400
        return("Insufficient points value !!",int(status_code),content_header)
    else:
        points_list = []
        while(points_to_deduct > 0):
            transaction = transactions.pop()
            points_to_deduct-= transaction[1]
            if points_to_deduct < 0:
                points_deducted = transaction[1] + points_to_deduct
                transaction[1]=points_deducted
                transactions.append(transaction)
            else:
                points_deducted = transaction[1]
            transaction[1] = points_deducted    
            transaction[2] = "now"
            points_list.append(transaction)
            accounts[transaction[0]]-= points_deducted
            total_points-= points_deducted
    
    for value in points_list:
        value[1] = -value[1]
    return jsonify(points_list)

@app.route("/balance",methods=['GET'])
def balance():
    """
    This is a REST endpoint to return point balance per user that would list all positive points per payer

    Returns:
        JSON object: Returns a JSON object of dictionary that provides the balance points of each payer
    """
    return jsonify(accounts)

if __name__ == "__main__":
    '''
    Starting the Flask application'''
    app.run(debug=True)