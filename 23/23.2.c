#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>


#define LEN (1000000)
#define LAST(removed) (removed->next->next)

typedef struct Node {
    uint64_t value;
    struct Node* next;
} Node;


static Node * list;

Node * create_list(uint64_t * data)
{

    Node * result = calloc(LEN, sizeof(Node));
    for(uint64_t i = 0; i < 9; i++)
    {
        result[i].value = data[i];
        result[i].next = &result[i+1];
    }

    for(uint64_t i = 9; i <= LEN; i++)
    {
        result[i].value = i + 1;
        result[i].next = &result[i+1];
    }

    result[LEN-1].next = &result[0];

    return result;
}

Node * do_remove(Node * current)
{
    Node * first_removed = current->next;
    Node * next_in = LAST(first_removed)->next;
    current->next = next_in;
    return first_removed;
}

int in_removed(uint64_t value, Node * removed)
{
    return removed->value == value || removed->next->value == value || removed->next->next->value == value;
}

uint64_t find_destination_value(uint64_t current_value, Node * removed)
{
    uint64_t destination;
    if(current_value == 1)
    {
        destination = LEN;
    }
    else
    {
        destination = current_value - 1;
    }

    while(in_removed(destination, removed))
    {
        if(destination == 1)
            destination = LEN;
        else
            destination--;
    }

    return destination;
}

uint64_t get_destination_index(uint64_t value)
{
    switch(value)
    {
    case 3:
        return 0;
    case 1:
        return 1;
    case 5:
        return 2;
    case 6:
        return 3;
    case 7:
        return 4;
    case 9:
        return 5;
    case 8:
        return 6;
    case 2:
        return 7;
    case 4:
        return 8;
    default:
        return value - 1;
    }
}

Node * get_destination(uint64_t value)
{
    return &list[get_destination_index(value)];
}

void insert_removed(Node * destination, Node * removed)
{
    LAST(removed)->next = destination->next;
    destination->next = removed;
}

Node * do_round(Node * current)
{
    Node * removed = do_remove(current);
    uint64_t destination_value = find_destination_value(current->value, removed);
    Node * destination = get_destination(destination_value);
    insert_removed(destination, removed);
    return current->next;
}


int main(void)
{
    uint64_t data[] = {3, 1, 5, 6, 7, 9, 8, 2, 4};
    list = create_list(data);
    Node * one = &list[1];
    Node * current = list;
    for(uint32_t i = 0; i < 10000000; i++)
    {
        current = do_round(&current[0]);
    }
    uint64_t first = one->next->value;
    uint64_t second = one->next->next->value;
    printf("%ld * %ld = %ld\n", first, second, first * second);
    free(list);
}
