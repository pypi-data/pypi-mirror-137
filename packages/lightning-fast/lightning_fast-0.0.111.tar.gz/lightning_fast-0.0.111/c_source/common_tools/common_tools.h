//
// Created by 徐秋实 on 2020/9/21.
//
#ifndef FAST_TOOLS_C_SOURCE_COMMON_TOOLS_H
#define FAST_TOOLS_C_SOURCE_COMMON_TOOLS_H

struct Chain {
    int val;
    struct Chain *next;
};

struct ListNode {
    int val;
    struct ListNode *next;
};

struct ChainInfo {
    struct Chain *start;
    struct Chain *end;
    int length;
};

struct Chain * convert_list_to_chain(const int values[], int length);

struct ListNode * convert_list_to_list_node_chain(const int values[], int length);

void delete_chain(struct Chain chain);

struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
    struct TreeNode *next;
};

void convert_list_to_tree(
        struct TreeNode *standby_nodes[],
        int standby_nodes_length,
        const int values[],
        int value_length,
        int current_value_index
);

void * free_tree(struct TreeNode * root);

void print_2d_tree(struct TreeNode *root, int space);


void draw_tree_hor(struct TreeNode *tree);

void print_2d_array(int ** array, int array_size, const int * column_sizes);

char* itoa(int val, int base);

void print_title(char title[], int length, char color[], char fix_char);

void draw_int_list(int * list, int length);

void draw_int_intervals(int ** intervals, int interval_size);

void draw_int_chain_list(struct ListNode * head);

#endif //FAST_TOOLS_C_SOURCE_COMMON_TOOLS_H
