import hashlib
from getpass import getpass
import pymysql


class BankServer:
    def __init__(self):
        self.DB_USER = 'root'
        self.DB_PASS = ''
        self.DB_NAME = 'bank_hash'
        self.DB_ADDRESS = 'localhost'
        self.connect_db()

    def hashing(self, acc_no, ifsc):
        hash_val = ifsc+str(acc_no)
        encoded_bytes = hash_val.encode()
        return hashlib.sha256(encoded_bytes)

    def print_hash(self, hashed_val):
        return hashed_val.hexdigest()

    def connect_db(self):
        self.db = pymysql.connect(self.DB_ADDRESS, self.DB_USER,
                                  self.DB_PASS, self.DB_NAME)
    
    def close(self):
        self.db.close()

    def store_payee(self, data):
        cursor = self.db.cursor()
        ref_name, acc_no, ifsc_code, hash_val = list(data.values())
        # check if account exists
        query = "SELECT 1 FROM users_secure WHERE acc_no=%s AND ifsc='%s'" % (acc_no,ifsc_code)
        try:
            # Execute the SQL command
            cursor.execute(query)
            # Fetch all the rows in a list of lists.
            result = cursor.fetchone()
            if result == None:
                print("Payee account does not exist")
                return False
        except Exception:
            print ("Error: unable to fetch data")
            return False

        query = "INSERT INTO payee_vulnerable VALUES (%s,'%s',%s,'%s')" % (
            self.session_user_id, ref_name, acc_no, ifsc_code)
        try:
            # Execute the SQL command
            cursor.execute(query)
            # Commit your changes in the database
            self.db.commit()
        except Exception as e:
            # Rollback in case there is any error
            print(e.args)
            self.db.rollback()
            return False

        query = "INSERT INTO payee_secure VALUES (%s,'%s','%s')" % (
            self.session_user_id, ref_name, hash_val)
        try:
            # Execute the SQL command
            cursor.execute(query)
            # Commit your changes in the database
            self.db.commit()
        except Exception as e:
            # Rollback in case there is any error
            print(e.args)
            self.db.rollback()
            return False
        return True


    def process_payee(self, user_id, data):
        print('Data received by server: '+str(data))
        self.session_user_id = user_id
        received_hash = data['hash']
        calc_hash = self.print_hash(self.hashing(data['acc_no'], data['ifsc']))
        print("Comparing hashes...\nReceived hash: "+received_hash+"\nCalculated hash on server side: "+calc_hash)

        if received_hash == calc_hash:
            print("Hashes match!")
            return self.store_payee(data)
        else:
            print("Hashes don't match. Please enter correct account number in both fields")
            return False
    
    def get_payee_list(self,user_id):
        cursor = self.db.cursor()
        query = "SELECT payee_ref_name FROM payee_vulnerable WHERE user_id="+str(user_id)
        try:
            # Execute the SQL command
            cursor.execute(query)
            # Fetch all the rows in a list of lists.
            results = cursor.fetchall()
            return results
        except Exception:
            print ("Error: unable to fetch payees")
            return None
    
    def get_payee_details(self,user_id,payee_name):
        cursor = self.db.cursor()
        query = "SELECT payee_acc_no, payee_ifsc FROM payee_vulnerable WHERE user_id=%d AND payee_ref_name='%s'" % (user_id,payee_name)
        try:
            # Execute the SQL command
            cursor.execute(query)
            # Fetch all the rows in a list of lists.
            result = cursor.fetchone()
            return result[0], result[1]
        except Exception:
            print ("Error: unable to fetch payee details")
        
    
    def get_payee_hash(self,user_id,payee_name):
        cursor = self.db.cursor()
        query = "SELECT payee_hash FROM payee_secure WHERE user_id=%d AND payee_ref_name='%s'" % (user_id,payee_name)
        try:
            # Execute the SQL command
            cursor.execute(query)
            # Fetch all the rows in a list of lists.
            result = cursor.fetchone()
            return result[0]
        except Exception:
            print ("Error: unable to fetch payee details")
        
    
    def _transfer(self,acc_no,amount):
        cursor = self.db.cursor()
        query = "SELECT acc_no FROM users_secure WHERE id="+str(self.session_user_id)
        try:
            # Execute the SQL command
            cursor.execute(query)
            # Fetch all the rows in a list of lists.
            result = cursor.fetchone()
            user_acc_no = result[0]
        except Exception:
            print ("Error: unable to fetch account details")
            return False
        
        query_debit = "UPDATE users_secure SET balance=balance-%d WHERE acc_no=%d"%(amount,user_acc_no)
        query_credit = "UPDATE users_secure SET balance=balance+%d WHERE acc_no=%d"%(amount,acc_no)
        try:
            # Execute the SQL command
            cursor.execute(query_debit)
            cursor.execute(query_credit)
            # Commit your changes in the database
            self.db.commit()
        except Exception as e:
            # Rollback in case there is any error
            print(e.args)
            self.db.rollback()
            return False
        
        return True
        

    def transfer_funds(self,user_id,data):
        print('Data received by server: '+str(data))
        self.session_user_id = user_id
        payee_acc_no,payee_ifsc = self.get_payee_details(user_id,data['payee'])
        payee_hash = self.get_payee_hash(user_id,data['payee'])
        calc_hash = self.print_hash(self.hashing(payee_acc_no,payee_ifsc))
        print("Retrieved hash -> "+payee_hash+"\nCalculated hash -> "+calc_hash)
        if payee_hash == calc_hash:
            print("Hashes match! Continuing funds transfer...")
            return self._transfer(payee_acc_no,data['amount'])
        else:
            print("REQUEST BLOCKED: Payee details do not match database. Retrieved and calculated hashes do not match.")
            return False


class BankClient:
    def __init__(self):
        self.id = 1

    def hashing(self, acc_no, ifsc):
        hash_val = ifsc+str(acc_no)
        encoded_bytes = hash_val.encode()
        return hashlib.sha256(encoded_bytes)

    def print_hash(self, hashed_val):
        return hashed_val.hexdigest()

    def add_payee(self):
        print("\nADD PAYEE\n")
        payee_ref = input("Enter payee's reference name: ")
        acc_to_hash = getpass("Enter payee's account number: ")
        print("(User entered account number -> "+acc_to_hash+")")
        acc_no = int(input("Confirm payee's account number: "))
        ifsc_code = input("Enter IFSC Code: ")

        print("Hashing masked account number and IFSC code...")
        hashed_val = self.hashing(acc_to_hash, ifsc_code)
        print("Hashed value on client side -> "+self.print_hash(hashed_val))

        data = {'ref_name': payee_ref, 'acc_no': acc_no, 'ifsc': ifsc_code,
                'hash': self.print_hash(hashed_val)}
        return data
    
    def transfer_money(self,payees):
        print("\nTRANSFER FUNDS\nPayees:")
        if payees == None:
            print("No payees. Please add a payee first")
        else:
            i = 1
            for row in payees:
                print(str(i)+". "+str(row[0]))
                i+=1
            payee_name = input("Enter payee name: ")
            amount = int(input("Enter amount to transfer: "))
            print("Transferring Rs. %d to %s..." % (amount,payee_name))
            return {'payee':payee_name,'amount':amount}


client = BankClient()
server = BankServer()
op = int(input("ABC Bank - Hashing demonstration\nChoose transaction\n1. Add payee\n2. Transfer funds\n"))
if op==1:
    data_map = client.add_payee()
    result = server.process_payee(client.id, data_map)
    if result:
        print("Payee added succesfully!")
    else:
        print("Adding payee failed")
elif op==2:
    payees = server.get_payee_list(client.id)
    data_map = client.transfer_money(payees)
    if data_map != None:
        result = server.transfer_funds(client.id,data_map)
        if result:
            print("Transaction successful!")
        else:
            print("Transaction failed")
else:
    print("Invalid option!")

server.close()

