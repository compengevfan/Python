#Parameters: 
#   Environment
#   Username
#   Password
#   Server/Array Name
#   Port/Director Identifier.
#Looks for the server/array name in the port listing to get the WWN.
#Create the alias with appropriate name.
import argparse
import BrocadeFunctions as BF

def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', required=True, action='store', help='PROD, DEV, DR')
    parser.add_argument('-u', required=True, action='store', help='Username')
    parser.add_argument('-p', required=True, action='store', help='Password')
    parser.add_argument('-n', required=True, action='store', help='Server or Array Name')
    parser.add_argument('-i', required=True, action='store', help='Port or Director Identifier')
    args = parser.parse_args()
    return args

def main():
    args = getargs()

    #print(args.e + '-' + args.u + '-' + args.p + '-' + args.n + '-' + args.i)

    IP1, IP2 = BF.BrocadeEnvironment(args.e)
    
    Connection1, Header1 = BF.BrocadeConnect(args.u, args.p, IP1)
    Connection2, Header2 = BF.BrocadeConnect(args.u, args.p, IP2)

    Delay1 = BF.BrocadeThrottle(Connection1)
    Delay2 = BF.BrocadeThrottle(Connection2)

    Disconnect1 = BF.BrocadeDisconnect(Connection1)
    if Disconnect1.get('http-resp-code') == 204:
        print("Switch1 session terminated.")
    Disconnect2 = BF.BrocadeDisconnect(Connection2)
    if Disconnect2.get('http-resp-code') == 204:
        print("Switch2 session terminated.")

if __name__ == "__main__":
    main()
