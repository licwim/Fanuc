/* ************************************************* */
/*                                                   */
/*    ───╔═╗──╔══╗╔══╗╔═╗╔═╗╔═╗╔══╗╔═╗─────╔═╗───    */
/*    ───║ ║──╚╗╔╝║╔═╝║ ║║ ║║ ║╚╗╔╝║ ║─────║ ║───    */
/*    ───║ ║───║║─║║──║ ║║ ║║ ║─║║─║ ╚═╗ ╔═╝ ║───    */
/*    ───║ ║───║║─║║──║ ║║ ║║ ║─║║─║ ╔═╗ ╔═╗ ║───    */
/*    ───║ ╚═╗╔╝╚╗║╚═╗║ ╚╝ ╚╝ ║╔╝╚╗║ ║ ╚═╝ ║ ║───    */
/*    ───╚═══╝╚══╝╚══╝╚══╝ ╚══╝╚══╝╚═╝─────╚═╝───    */
/*                                                   */
/*   main.c                                          */
/*       By: licwim                                  */
/*                                                   */
/*   Created: 14-12-2019 15:18:30 by licwim          */
/*   Updated: 14-12-2019 15:19:43 by licwim          */
/*                                                   */
/* ************************************************* */

#include "../head/fanuc.h"

int					error(int errcode)
{
	if (errcode == FILE_OPEN_ERROR)
		printf("File open error.\n");
	if (errcode == DIR_CREATE_ERROR)
		printf("Error creating directory for backups.\n");
	if (errcode == FILE_CREATE_ERROR)
		printf("Error creating backup file.\n");

	exit (1);
}

void				backup(const char *filename)
{
	FILE	*src;
	FILE	*dst;
	char	buf[BUFSIZ];
	size_t	nread;

	if (!(src = fopen(filename, "rb")))
		error (FILE_OPEN_ERROR);
	if (chdir("backups") == -1)
	{
		if (mkdir("backups") == -1)
			error (DIR_CREATE_ERROR);
		chdir("backups");
	}
	if (!(dst = fopen(filename, "wb")))
		error (FILE_CREATE_ERROR);
	while(nread = fread(buf, sizeof(char), sizeof(buf), src))
		fwrite(buf, sizeof(char), nread, dst);
	fclose(src);
	fclose(dst);
	chdir("..");
}

int					main(int arc, char **arv)
{
	int		fd;

	// printf("%s\n", arv[1]);
	backup("test");
	// converter(arv[1]);
	return (0);
}
