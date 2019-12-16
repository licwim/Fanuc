/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kdune <marvin@42.fr>                       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/04/18 01:09:50 by kdune             #+#    #+#             */
/*   Updated: 2019/06/27 23:46:56 by kdune            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

char	*bufdel(char *stat_buf, char *buf, int act)
{
	char	*tmp;

	if (act == 1)
	{
		tmp = stat_buf;
		if (!(stat_buf = ft_strdup(ft_strchr(stat_buf, '\n') + 1)))
			return (NULL);
		ft_strdel(&tmp);
	}
	else
	{
		tmp = stat_buf;
		if (!(stat_buf = ft_strjoin(stat_buf, buf)))
			return (NULL);
		ft_strdel(&tmp);
	}
	return (stat_buf);
}

int		gnl_return(char **stat_buf, char **line, char *end)
{
	int	len;

	if (end)
	{
		len = ft_strchr(*stat_buf, '\n') - *stat_buf;
		if (!(*line = ft_strnew(len)))
			return (-1);
		ft_strncpy(*line, *stat_buf, len);
	}
	else if (*stat_buf && **stat_buf)
	{
		if (!(*line = ft_strdup(*stat_buf)))
			return (-1);
		ft_strdel(stat_buf);
	}
	else
	{
		ft_strdel(stat_buf);
		return (0);
	}
	return (1);
}

int		get_next_line(const int fd, char **line)
{
	static char	*stat_buf[FD_SIZE];
	char		buf[BUFF_SIZE + 1];
	char		*end;
	int			bt;

	end = NULL;
	if ((bt = 1) && fd >= 0 && fd < FD_SIZE && stat_buf[fd])
	{
		if (!(stat_buf[fd] = bufdel(stat_buf[fd], buf, 1)))
			return (-1);
		end = ft_strchr(stat_buf[fd], '\n');
	}
	while (!end && (bt = read(fd, buf, BUFF_SIZE)))
	{
		if (bt < 0 || (buf[bt] = 0))
			return (-1);
		if (stat_buf[fd])
			if (!(stat_buf[fd] = bufdel(stat_buf[fd], buf, 2)))
				return (-1);
		if (!stat_buf[fd])
			if (!(stat_buf[fd] = ft_strdup(buf)))
				return (-1);
		end = ft_strchr(buf, '\n');
	}
	return (gnl_return(&stat_buf[fd], line, end));
}
