/* ************************************************* */
/*                                                   */
/*    ───╔═╗──╔══╗╔══╗╔═╗╔═╗╔═╗╔══╗╔═╗─────╔═╗───    */
/*    ───║ ║──╚╗╔╝║╔═╝║ ║║ ║║ ║╚╗╔╝║ ║─────║ ║───    */
/*    ───║ ║───║║─║║──║ ║║ ║║ ║─║║─║ ╚═╗ ╔═╝ ║───    */
/*    ───║ ║───║║─║║──║ ║║ ║║ ║─║║─║ ╔═╗ ╔═╗ ║───    */
/*    ───║ ╚═╗╔╝╚╗║╚═╗║ ╚╝ ╚╝ ║╔╝╚╗║ ║ ╚═╝ ║ ║───    */
/*    ───╚═══╝╚══╝╚══╝╚══╝ ╚══╝╚══╝╚═╝─────╚═╝───    */
/*                                                   */
/*   converter.c                                     */
/*       By: licwim                                  */
/*                                                   */
/*   Created: 14-12-2019 16:50:17 by licwim          */
/*   Updated: 14-12-2019 16:50:41 by licwim          */
/*                                                   */
/* ************************************************* */

#include "fanuc.h"

void	converter(char *filename)
{
	int		fd;
	char	*buf;
	long	filesize;

	backup(filename);
	if (fd = open(filename, O_RDONLY))
		error (FILE_OPEN_ERROR);
	// while (get_next_line())
	// fseek(fs, 0, SEEK_END);
	// filesize = ftell(fs);
	close(fd);
}