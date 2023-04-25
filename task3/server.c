#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#include <pthread.h>
#include <ctype.h>
#define PORT 8080

struct Stack {
    int top;
    int capacity;
    float* array;
};

struct Stack* createStack(int capacity)
{
    struct Stack* stack = (struct Stack*)malloc(sizeof(struct Stack));
 
    if (!stack)
        return NULL;
 
    stack->top = -1;
    stack->capacity = capacity;
    stack->array = (float*)malloc(stack->capacity * sizeof(float));
 
    if (!stack->array)
        return NULL;
 
    return stack;
}


int isEmpty(struct Stack* stack)
{
    return stack->top == -1;
}
 
float pop(struct Stack* stack)
{
    if (!isEmpty(stack))
        return stack->array[stack->top--];
    return -1.0;
}
 
void push(struct Stack* stack, float op)
{
    stack->array[++stack->top] = op;
}

float eval_float(char* str) {
    float value = atof(str);
    return value;
}

void float_to_string(float value, char* response, int precision) {
    sprintf(response, "%.*f", precision, value);
}

char* handleRequest(char* exp){
    struct Stack* stack = createStack(strlen(exp));
 
    if (!stack)
        return "-1";

    char* token = strtok(exp," ");
    while(token != NULL){

        if(!strcmp(token,"0"))
            push(stack, eval_float(token));
        else if(eval_float(token) != 0.000000)
            push(stack, eval_float(token));

        else {
            float val1 = pop(stack);
            float val2 = pop(stack);
            if(!strcmp(token,"+")){
                push(stack, val2 + val1);
            }
            else if(!strcmp(token,"-")){
                push(stack, val2 - val1);
            }
            else if(!strcmp(token,"*")){
                push(stack, val2 * val1);
            }
            else if(!strcmp(token,"/")){
                push(stack, val2 / val1);
            }
            else{
                printf("Invalid Expression\n");
                break;
            }
        }

        token = strtok(NULL," ");
    }

    char* response = (char*)malloc(1024*sizeof(char));
    float_to_string(pop(stack), response, 6);
    return response;
}

void *handle_connection(void *arg){
    
    int socketId = *((int *)arg);  
    //read request
    while(1){
        char buffer[1024] = { 0 };
        int valread = read(socketId, buffer, 1024);
        printf("%s\n", buffer);

        if(!strcmp(buffer,"quit")){
            close(socketId);
            return NULL;
        }
        
        // pthread_mutex_t lock;
        // pthread_mutex_init(&lock, NULL);
        // pthread_mutex_lock(&lock);
        // FILE *fp;
        // fp = fopen("server_records.txt","a");
        // fprintf(fp,"Request By Client ID: %d ,",socketId);
        // fclose(fp);
        // pthread_mutex_unlock(&lock);

        char* response = handleRequest(buffer);
        //send response
        send(socketId, response, strlen(response), 0);
    }
}

int main(int argc, char const* argv[])
{
    //login into the server
    printf("Enter User ID: ");
	char userID[10] = {0};
	scanf("%s",userID);
	printf("Enter Password: ");
	char Password[10] = {0};
	scanf("%s",Password);
    if(!strcmp(userID,"agent") && !strcmp(Password,"123")){
        printf("Logged In Successfully.\n");

        int server_fd, new_socket;
        struct sockaddr_in address;
        int opt = 1;
        int addrlen = sizeof(address);

        // Creating socket file descriptor
        if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
            perror("socket failed");
            exit(EXIT_FAILURE);
        }

        // Forcefully attaching socket to the port 8080
        if (setsockopt(server_fd, SOL_SOCKET,
                    SO_REUSEADDR | SO_REUSEPORT, &opt,
                    sizeof(opt))) {
            perror("setsockopt");
            exit(EXIT_FAILURE);
        }
        address.sin_family = AF_INET;
        address.sin_addr.s_addr = INADDR_ANY;
        address.sin_port = htons(PORT);

        // Forcefully attaching socket to the port 8080
        if (bind(server_fd, (struct sockaddr*)&address,
                sizeof(address))
            < 0) {
            perror("bind failed");
            exit(EXIT_FAILURE);
        }
        if (listen(server_fd, 3) < 0) {
            perror("listen");
            exit(EXIT_FAILURE);
        }
        printf("Listening.......\n");

        while(1){
            if ((new_socket = accept(server_fd, (struct sockaddr*)&address,(socklen_t*)&addrlen))< 0) {
                perror("accept");
                exit(EXIT_FAILURE);
            }

            pthread_t client_threadid;
            pthread_create(&client_threadid,NULL,handle_connection,&new_socket);
        }

        // closing the listening socket
        shutdown(server_fd, SHUT_RDWR);

    }
    else{
        printf("Wrong Credentials.\n");
    }
    
	return 0;
}