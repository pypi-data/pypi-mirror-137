//
// Created by 徐秋实 on 2020/9/21.
//
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "common_tools.h"
#include "tests/label_encoder_test/error.h"
#include <errno.h>

struct Chain *convert_list_to_chain(const int values[], int length) {
    struct Chain *start_node = (struct Chain *) malloc(sizeof(struct Chain));
    struct Chain *current_node;
    current_node = start_node;
    for (int i = 0; i < length; i++) {
        if (i == 0) {
            current_node->val = values[i];
        } else {
            struct Chain *new_node = (struct Chain *) malloc(sizeof(struct Chain));
            new_node->val = values[i];
            current_node->next = new_node;
            current_node = new_node;
        }
    }
    current_node->next = NULL;
    return start_node;
}

struct ListNode *convert_list_to_list_node_chain(const int values[], int length) {
    struct ListNode *start_node = (struct ListNode *) malloc(sizeof(struct ListNode));
    struct ListNode *current_node;
    current_node = start_node;
    for (int i = 0; i < length; i++) {
        if (i == 0) {
            current_node->val = values[i];
        } else {
            struct ListNode *new_node = (struct ListNode *) malloc(sizeof(struct ListNode));
            new_node->val = values[i];
            current_node->next = new_node;
            current_node = new_node;
        }
    }
    current_node->next = NULL;
    return start_node;
}

void delete_chain(struct Chain chain) {
    struct Chain *current_chain = &chain;
    while (NULL != current_chain) {
        struct Chain *copy_current_chain = current_chain;
        current_chain = current_chain->next;
        free(copy_current_chain);
    }
}

void convert_list_to_tree(
        struct TreeNode *standby_nodes[],
        int standby_nodes_length,
        const int values[],
        int value_length,
        int current_value_index
) {
    if (standby_nodes_length == 0) {
        return;
    }
    int difference_between = value_length - 2 * standby_nodes_length - current_value_index;
    int new_standby_length;
    if (difference_between >= 0) {
        new_standby_length = 2 * standby_nodes_length;
    } else {
        new_standby_length = value_length - current_value_index;
    }
    struct TreeNode *new_standby_nodes[new_standby_length];
    int new_position;
    for (int i = 0; i < standby_nodes_length; i++) {
        if (NULL == standby_nodes[i]) {
            continue;
        }

        if ((i * 2 + current_value_index < value_length)) {
            if ((-1 != values[i * 2 + current_value_index])) {
                struct TreeNode *left;
                left = (struct TreeNode *) malloc(sizeof(struct TreeNode));
                left->val = values[i * 2 + current_value_index];
                left->left = NULL;
                left->right = NULL;
                standby_nodes[i]->left = left;
                new_standby_nodes[i * 2] = left;
            } else {
                new_standby_nodes[i * 2] = NULL;
            }
            new_position = i * 2 + current_value_index + 1;
        }
        if ((i * 2 + current_value_index + 1 < value_length)) {
            if ((-1 != values[i * 2 + current_value_index + 1])) {
                struct TreeNode *right;
                right = (struct TreeNode *) malloc(sizeof(struct TreeNode));
                right->val = values[i * 2 + current_value_index + 1];
                right->left = NULL;
                right->right = NULL;
                standby_nodes[i]->right = right;
                new_standby_nodes[i * 2 + 1] = right;
            } else {
                new_standby_nodes[i * 2 + 1] = NULL;
            }
            new_position = i * 2 + current_value_index + 2;
        }
    }
    int correct_standby_length = new_standby_length;
    int j = 0;
    while (j < correct_standby_length) {
        if (NULL == new_standby_nodes[j]) {
            // 这里new_standby_length需要减一，否则有内存访问问题。
            for (int k = j; k < new_standby_length - 1; k++) {
                new_standby_nodes[k] = new_standby_nodes[k + 1];
            }
            correct_standby_length -= 1;
        } else {
            j++;
        }
    }
    convert_list_to_tree(new_standby_nodes, correct_standby_length, values, value_length, new_position);
}

void *free_tree(struct TreeNode *root) {
    if (NULL == root) {
        return NULL;
    }
    free_tree(root->left);
    free_tree(root->right);
    free(root);
    root = NULL;
    return NULL;
}


void print_2d_tree(struct TreeNode *root, int space) {
    // Base case
    if (root == NULL)
        return;

    // Increase distance between levels
    space += 10;

    // Process right child first
    print_2d_tree(root->right, space);

    // Print current node after space
    // count
    printf("\n");
    for (int i = 10; i < space; i++)
        printf(" ");
    printf("%d\n", root->val);

    // Process left child
    print_2d_tree(root->left, space);
}

void draw_tree_hor2(struct TreeNode *tree, int depth, char *path, int right) {
    // stopping condition
    if (tree == NULL)
        return;

    // increase spacing
    depth++;

    // start with right node
    draw_tree_hor2(tree->right, depth, path, 1);

    if (depth > 1) {
        // set | draw map
        path[depth - 2] = 0;

        if (right)
            path[depth - 2] = 1;
    }

    if (tree->left)
        path[depth - 1] = 1;

    // print root after spacing
    printf("\n");

    for (int i = 0; i < depth - 1; i++) {
        if (i == depth - 2)
            printf("+");
        else if (path[i])
            printf("|");
        else
            printf(" ");

        for (int j = 1; j < 10; j++)
            if (i < depth - 2)
                printf(" ");
            else
                printf("-");
    }

    printf("%d\n", tree->val);

    // vertical spacers below
    for (int i = 0; i < depth; i++) {
        if (path[i])
            printf("|");
        else
            printf(" ");

        for (int j = 1; j < 10; j++)
            printf(" ");
    }

    // go to left node
    draw_tree_hor2(tree->left, depth, path, 0);
}

void draw_tree_hor(struct TreeNode *tree) {
    // should check if we don't exceed this somehow..
    char path[255] = {};

    //initial depth is 0
    draw_tree_hor2(tree, 0, path, 0);
    printf("\n");
}

void print_2d_array(int **array, int array_size, const int *column_sizes) {
    printf("[\n");
    for (int i = 0; i < array_size; i++) {
        printf("\t");
        for (int j = 0; j < column_sizes[i]; j++) {
            printf("%d, ", array[i][j]);
        }
        printf("\n");
    }
    printf("]\n");
}

char *itoa(int val, int base) {

    static char buf[32] = {0};

    int i = 30;

    for (; val && i; --i, val /= base)

        buf[i] = "0123456789abcdef"[val % base];

    return &buf[i + 1];

}

void print_title(char title[], int length, char color[], char fix_char) {
    if (strcmp(color, "yellow") == 0) {
        printf("\033[0;33m");
    } else if (strcmp(color, "blue") == 0) {
        printf("\033[0;34m");
    } else {
        errno = CUSTOM_ERROR;
        fprintf(stderr, "自定义错误: 输入了不存在的颜色选项\n");
        exit(EXIT_FAILURE);
    }
    const int total_length = length;
    char prefix[100];
    char suffix[100];
    int string_length = (int) strlen(title);
    int prefix_length = (total_length - string_length) / 2;
    int suffix_length = total_length - prefix_length - string_length;
    for (int i = 0; i < prefix_length; i++) {
        prefix[i] = fix_char;
    }
    prefix[prefix_length] = '\0';
    for (int i = 0; i < suffix_length; i++) {
        suffix[i] = fix_char;
    }
    suffix[suffix_length] = '\0';
    printf("%*s%*s%*s\n", prefix_length, prefix, string_length, title, suffix_length, suffix);
    printf("\033[0m");
};

void draw_int_list(int * list, int length) {
    printf("[\n\t");
    for (int i=0; i<length; i++) {
        printf("%d, ", list[i]);
    }
    printf("\n]\n");
}

void draw_int_intervals(int ** intervals, int interval_size) {
    printf("[\n\t");
    for (int i=0; i<interval_size; i++) {
        printf("[%d, %d], ", intervals[i][0], intervals[i][1]);
    }
    printf("\n]\n");
}

void draw_int_chain_list(struct ListNode * head) {
    struct ListNode * tmp;
    tmp = head;
    printf("\n");
    while(tmp) {
        if (tmp->next) {
            printf("%d -> ", tmp->val);
        } else {
            printf("%d", tmp->val);
        }
        tmp = tmp->next;
    }
    printf("\n");
}
