
#ifndef FANUC_H
# define FANUC_H

#define FILE_OPEN_ERROR 1
#define DIR_CREATE_ERROR 2
#define FILE_CREATE_ERROR 3

#include <stdio.h>
#include <io.h>
// #include <dir.h>
#include <stdlib.h>
#include "get_next_line.h"
#include "libft.h"

void	converter(char *filename);
void	backup(const char *filename);
int		error(int errcode);


#endif
