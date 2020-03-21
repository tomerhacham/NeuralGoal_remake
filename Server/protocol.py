class protocol:
    terminate=False

    def execute(self,command):
        response=command
        print("the command is: {}".format(command))
        if command=='germany':
            print(command)        
        elif command=='england':
            print(command)        
        elif command=='italy':
            print(command)        
        elif command=='spain':
            print(command)        
        elif command=='franch':
            print(command)
        elif command=='disconnect':
            print(command)
            self.terminate=True
            response='Disconnected'
        else:
            print(command)
            response='Invalid command'
        return response


                             
