Namespaces, Organize your teams and projects


Digicloud Namespace allows you to organize your resources. For example if you have separate teams working on different projects
 or you want to keep different environments (like production, staging, QA) fully separated, Then you can use Digicloud namespaces. 
Every Namespace has its members and is also billed separately. 

## Examples


1. **Creating a namespace**
    
    You can create a namespace by using the following command, you just need to choose a name, for example myblog:

        $ digicloud namespace create myblog

2. **Listing your namespaces**
    
    Every user could be a member of different namespaces, you can check all your current namespaces:

        $ digicloud namespace list

3. **Current Namespace**
    
    In order to manage different namespaces using CLI, you should check and change active namespace in your CLI. to check 
your active namespace you can use:

        $ digicloud namespace current
    
    and to change it you can use:
 
        $ digicloud namespace select myblog
