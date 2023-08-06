
import copy
import numpy as np
from scipy.interpolate import interp1d
import matplotlib as mpl
from datetime import date, datetime, timezone
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import warnings
import pytplot
from fnmatch import filter as tname_filter

# the following improves the x-axis ticks labels
import matplotlib.units as munits
import matplotlib.dates as mdates
converter = mdates.ConciseDateConverter()
munits.registry[np.datetime64] = converter
munits.registry[date] = converter
munits.registry[datetime] = converter

def tplot(variables, var_label=None,
                     xsize=8, 
                     ysize=10, 
                     save_png='', 
                     save_eps='', 
                     save_svg='', 
                     save_pdf='', 
                     display=True, 
                     fig=None, 
                     axis=None, 
                     pseudo_plot_num=None, 
                     pseudo_right_axis=False,
                     pseudo_yaxis_options=None,
                     pseudo_zaxis_options=None,
                     pseudo_line_options=None,
                     pseudo_extra_options=None,
                     second_axis_size=0.0,
                     return_plot_objects=False):
    """
    This function creates tplot windows using matplotlib as a backend.
    """
    if isinstance(variables, str):
        # check for wild cards * or ?
        if '*' in variables or '?' in variables:
            tnames = pytplot.tplot_names(quiet=True)
            variables = tname_filter(tnames, variables)

    if not isinstance(variables, list):
        variables = [variables]
        
    num_panels = len(variables)

    if fig is None and axis is None:
        fig, axes = plt.subplots(nrows=num_panels, sharex=True)
        fig.set_size_inches(xsize, ysize)
    else:
        if pseudo_plot_num == 0 or pseudo_right_axis == False:
            # setting up first axis
            axes = axis
        else:
            # using previous axis
            axes = axis.twinx()
    
    plot_title = pytplot.tplot_opt_glob['title_text']
    axis_font_size = pytplot.tplot_opt_glob.get('axis_font_size')
    vertical_spacing = pytplot.tplot_opt_glob.get('vertical_spacing')
    xmargin = pytplot.tplot_opt_glob.get('xmargin')
    ymargin = pytplot.tplot_opt_glob.get('ymargin')
    zrange = [None, None]

    colorbars = {}

    if xmargin is None:
        xmargin = [0.10, 0.05]

    fig.subplots_adjust(left=xmargin[0], right=1-xmargin[1])

    if ymargin is not None:
        fig.subplots_adjust(top=1-ymargin[0], bottom=ymargin[1])

    if vertical_spacing is None:
        vertical_spacing = 0.07
    
    fig.subplots_adjust(hspace=vertical_spacing)
    
    for idx, variable in enumerate(variables):
        var_data_org = pytplot.get_data(variable)
        
        if var_data_org is None:
            print('Variable not found: ' + variable)
            continue

        var_data = copy.deepcopy(var_data_org)

        # plt.subplots returns a list of axes for multiple panels 
        # but only a single axis for a single panel
        if num_panels == 1:
            this_axis = axes
        else:
            this_axis = axes[idx]

        pseudo_var = False
        overplots = None
        spec = False

        var_quants = pytplot.data_quants[variable]

        if not isinstance(var_quants, dict):
            if var_quants.attrs['plot_options'].get('overplots_mpl') is not None:
                overplots = var_quants.attrs['plot_options']['overplots_mpl']
                pseudo_var = True

        # deal with pseudo-variables first
        if isinstance(var_data, list) or isinstance(var_data, str) or pseudo_var:
            # this is a pseudo variable
            if isinstance(var_data, str):
                var_data = var_data.split(' ')

            if pseudo_var:
                pseudo_vars = overplots
            else:
                pseudo_vars = var_data

            # pseudo variable metadata should override the metadata
            # for individual variables
            yaxis_options = None
            zaxis_options = None
            line_opts = None
            plot_extras = None
            if pseudo_var:
                plot_extras = var_quants.attrs['plot_options']['extras']
                if plot_extras.get('spec') is not None:
                    spec = True

                if plot_extras.get('right_axis') is not None:
                    if plot_extras.get('right_axis'):
                        pseudo_right_axis = True

                if pseudo_right_axis or spec:
                    plot_extras = None
                else:
                    yaxis_options = var_quants.attrs['plot_options']['yaxis_opt']
                    zaxis_options = var_quants.attrs['plot_options']['zaxis_opt']
                    line_opts = var_quants.attrs['plot_options']['line_opt']

            for pseudo_idx, var in enumerate(pseudo_vars):
                tplot(var, return_plot_objects=return_plot_objects, 
                        xsize=xsize, ysize=ysize, save_png=save_png, 
                        save_eps=save_eps, save_svg=save_svg, save_pdf=save_pdf, 
                        fig=fig, axis=this_axis, display=False, 
                        pseudo_plot_num=pseudo_idx, second_axis_size=0.1,
                        pseudo_yaxis_options=yaxis_options, pseudo_zaxis_options=zaxis_options,
                        pseudo_line_options=line_opts, pseudo_extra_options=plot_extras,
                        pseudo_right_axis=pseudo_right_axis)
            continue

        # the data are stored as unix times, but matplotlib wants datatime objects
        var_times = [datetime.fromtimestamp(time, tz=timezone.utc) for time in var_data.times]
        
        # set the figure title
        if idx == 0 and plot_title != '':
            this_axis.set_title(plot_title)
        
        # set the x-axis range, if it was set with xlim or tlimit
        if pytplot.tplot_opt_glob.get('x_range') is not None:
            x_range = pytplot.tplot_opt_glob['x_range']
            this_axis.set_xlim([datetime.fromtimestamp(x_range[0], tz=timezone.utc), datetime.fromtimestamp(x_range[1], tz=timezone.utc)])

        # set some more plot options
        if pseudo_yaxis_options is not None:
            yaxis_options = pseudo_yaxis_options
        else:
            yaxis_options = var_quants.attrs['plot_options']['yaxis_opt']

        if pseudo_zaxis_options is not None:
            zaxis_options = pseudo_zaxis_options
        else:
            zaxis_options = var_quants.attrs['plot_options']['zaxis_opt']

        if pseudo_line_options is not None:
            line_opts = pseudo_line_options
        else:
            line_opts = var_quants.attrs['plot_options']['line_opt']

        if pseudo_extra_options is not None:
            plot_extras = pseudo_extra_options
        else:
            plot_extras = var_quants.attrs['plot_options']['extras']

        ylog = yaxis_options['y_axis_type']
        if ylog == 'log':
            this_axis.set_yscale('log')
        else:
            this_axis.set_yscale('linear')
            
        ytitle = yaxis_options['axis_label']
        if ytitle == '':
            ytitle = variable
        
        if yaxis_options.get('axis_subtitle') is not None:
            ysubtitle = yaxis_options['axis_subtitle']
        else:
            ysubtitle = ''
            
        if axis_font_size is not None:
            this_axis.tick_params(axis='x', labelsize=axis_font_size)
            this_axis.tick_params(axis='y', labelsize=axis_font_size)

        if plot_extras.get('char_size') is not None:
            char_size = plot_extras['char_size']
        else:
            char_size = 14

        yrange = yaxis_options['y_range']
        if not np.isfinite(yrange[0]):
            yrange[0] = None
        if not np.isfinite(yrange[1]):
            yrange[1] = None

        this_axis.set_ylim(yrange)
        this_axis.set_ylabel(ytitle + '\n' + ysubtitle, fontsize=char_size)

        if plot_extras.get('alpha') is not None:
            alpha = plot_extras['alpha']
        else:
            alpha = None

        if plot_extras.get('border') is not None:
            border = plot_extras['border']
        else:
            border = True

        if border == False:
            this_axis.axis('off')

        # determine if this is a line plot or a spectrogram
        if plot_extras.get('spec') is not None:
            spec = plot_extras['spec']
        else:
            spec = False

        if not spec:
            # create line plots
            if yaxis_options.get('legend_names') is not None:
                labels = yaxis_options['legend_names']
                if labels[0] is None:
                    labels = None
            else:
                labels = None
            
            if len(var_data.y.shape) == 1:
                num_lines = 1
            else:
                num_lines = var_data.y.shape[1]

            # set up line colors
            if plot_extras.get('line_color') is not None:
                colors = plot_extras['line_color']
            else:
                if num_lines == 3:
                    colors = ['b', 'g', 'r']
                elif num_lines == 4:
                    colors = ['b', 'g', 'r', 'k']
                else:
                    colors = ['k', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']

                if num_lines >= len(colors):
                    colors = colors*num_lines

            # line thickness
            if line_opts.get('line_width') is not None:
                thick = line_opts['line_width']
            else:
                thick = 0.5

            # line style
            if line_opts.get('line_style_name') is not None:
                line_style_user = line_opts['line_style_name']
                # legacy values
                if line_style_user == 'solid_line':
                    line_style = 'solid'
                elif line_style_user == 'dot':
                    line_style = 'dotted'
                elif line_style_user == 'dash':
                    line_style = 'dashed'
                elif line_style_user == 'dash_dot':
                    line_style = 'dashdot'
                else:
                    line_style = line_style_user
            else:
                line_style = 'solid'

            # create the plot
            line_options = {'linewidth': thick, 'linestyle': line_style, 'alpha': alpha}

            # check for error data first
            if 'dy' in var_data._fields:
                # error data provided
                line_options['yerr'] = var_data.dy
                plotter = this_axis.errorbar
            else:
                # no error data provided
                plotter = this_axis.plot

            for line in range(0, num_lines):
                this_line = plotter(var_times, var_data.y if num_lines == 1 else var_data.y[:, line], color=colors[line], **line_options)

                if labels is not None:
                    if isinstance(this_line, list):
                        this_line[0].set_label(labels[line])
                    else:
                        this_line.set_label(labels[line])

            if labels is not None:
                this_axis.legend()
        else:
            # create spectrogram plots
            spec_options = {'shading': 'auto', 'alpha': alpha}
            ztitle = zaxis_options['axis_label']
            zlog = zaxis_options['z_axis_type']

            if zaxis_options.get('z_range') is not None:
                zrange = zaxis_options['z_range']
            else:
                zrange = [None, None]
                
            if zaxis_options.get('axis_subtitle') is not None:
                zsubtitle = zaxis_options['axis_subtitle']
            else:
                zsubtitle = ''
            
            if zlog == 'log':
                spec_options['norm'] = mpl.colors.LogNorm(vmin=zrange[0], vmax=zrange[1])
            else:
                spec_options['norm'] = None
                spec_options['vmin'] = zrange[0]
                spec_options['vmax'] = zrange[1]
            
            if plot_extras.get('colormap') is not None:
                cmap = plot_extras['colormap'][0]
            else:
                cmap = 'spedas'
            
            # kludge to add support for the 'spedas' color bar
            if cmap == 'spedas':
                _colors = pytplot.spedas_colorbar
                spd_map = [(np.array([r, g, b])).astype(np.float64)/256 for r, g, b in zip(_colors.r, _colors.g, _colors.b)]
                cmap = LinearSegmentedColormap.from_list('spedas', spd_map)
                
            spec_options['cmap'] = cmap

            out_values = var_data.y

            if len(var_data) == 3:
                out_vdata = var_data.v
            else:
                print('Too many dimensions on the variable: ' + variable)
                continue

            # automatic interpolation options
            if yaxis_options.get('x_interp') is not None:
                x_interp = yaxis_options['x_interp']

                # interpolate along the x-axis
                if x_interp:
                    if yaxis_options.get('x_interp_points') is not None:
                        nx = yaxis_options['x_interp_points']
                    else:
                        fig_size = fig.get_size_inches()*fig.dpi
                        nx = fig_size[0]

                    if zlog == 'log':
                        zdata = np.log10(out_values)
                    else:
                        zdata = out_values

                    zdata[zdata < 0.0] = 0.0
                    zdata[zdata == np.nan] = 0.0

                    interp_func = interp1d(var_data.times, zdata, axis=0, bounds_error=False)
                    out_times = np.arange(0, nx, dtype=np.float64)*(var_data.times[-1]-var_data.times[0])/(nx-1) + var_data.times[0]

                    out_values = interp_func(out_times)

                    if zlog == 'log':
                        out_values = 10**out_values

                    var_times = [datetime.fromtimestamp(time, tz=timezone.utc) for time in out_times]

            if yaxis_options.get('y_interp') is not None:
                y_interp = yaxis_options['y_interp']

                # interpolate along the y-axis
                if y_interp:
                    if yaxis_options.get('y_interp_points') is not None:
                        ny = yaxis_options['y_interp_points']
                    else:
                        fig_size = fig.get_size_inches()*fig.dpi
                        ny = fig_size[1]

                    if zlog == 'log':
                        zdata = np.log10(out_values)
                    else:
                        zdata = out_values

                    if ylog =='log':
                        vdata = np.log10(var_data.v)
                        ycrange = np.log10(yrange)
                    else:
                        vdata = var_data.v
                        ycrange = yrange

                    if not np.isfinite(ycrange[0]):
                        ycrange = [np.min(vdata), yrange[1]]

                    zdata[zdata < 0.0] = 0.0
                    zdata[zdata == np.nan] = 0.0

                    interp_func = interp1d(vdata, zdata, axis=1, bounds_error=False)
                    out_vdata = np.arange(0, ny, dtype=np.float64)*(ycrange[1]-ycrange[0])/(ny-1) + ycrange[0]

                    out_values = interp_func(out_vdata)

                    if zlog == 'log':
                        out_values = 10**out_values

                    if ylog == 'log':
                        out_vdata = 10**out_vdata

            # check for NaNs in the v values
            nans_in_vdata = np.argwhere(np.isfinite(out_vdata) == False)
            if len(nans_in_vdata) > 0:
                # to deal with NaNs in the energy table, we set those energies to 0
                # then apply a mask to the data values at these locations
                out_vdata_nonan = out_vdata.copy()
                times_with_nans = np.unique(nans_in_vdata[:, 0])
                for nan_idx in np.arange(0, len(times_with_nans)):
                    this_time_idx = times_with_nans[nan_idx]
                    out_vdata_nonan[this_time_idx, ~np.isfinite(out_vdata[this_time_idx, :])] = 0

                masked = np.ma.masked_where(~np.isfinite(out_vdata), out_values)
                out_vdata = out_vdata_nonan
                out_values = masked

            # check for negatives if zlog is requested
            if zlog =='log':
                out_values[out_values<0.0] = 0.0

            # create the spectrogram (ignoring warnings)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                im = this_axis.pcolormesh(var_times, out_vdata.T, out_values.T, **spec_options)

            # store everything needed to create the colorbars
            colorbars[variable] = {}
            colorbars[variable]['im'] = im
            colorbars[variable]['axis_font_size'] = axis_font_size
            colorbars[variable]['ztitle'] = ztitle
            colorbars[variable]['zsubtitle'] = zsubtitle
            
        # apply any vertical bars
        if pytplot.data_quants[variable].attrs['plot_options'].get('time_bar') is not None:
            time_bars = pytplot.data_quants[variable].attrs['plot_options']['time_bar']

            for time_bar in time_bars:
                this_axis.axvline(x=datetime.fromtimestamp(time_bar['location'], tz=timezone.utc), 
                    color=np.array(time_bar.get('line_color'))/256.0, lw=time_bar.get('line_width'))
    
    # apply any addition x-axes specified by the var_label keyword
    if var_label is not None:
        if not isinstance(var_label, list):
            var_label = [var_label]

        axis_delta = 0.0

        for label in var_label:
            label_data = pytplot.get_data(label, xarray=True)

            if label_data is None:
                print('Variable not found: ' + label)
                continue

            if len(label_data.values.shape) != 1:
                print(label + ' specified as a vector; var_label only supports scalars. Try splitting the vector into seperate tplot variables.')
                continue

            # set up the new x-axis
            axis_delta = axis_delta - num_panels*0.1
            new_xaxis = this_axis.secondary_xaxis(axis_delta)
            xaxis_ticks = this_axis.get_xticks().tolist()
            xaxis_ticks_dt = [mpl.dates.num2date(tick_val) for tick_val in xaxis_ticks]
            xaxis_ticks_unix = [tick_val.timestamp() for tick_val in xaxis_ticks_dt]
            xaxis_labels = get_var_label_ticks(label_data, xaxis_ticks_unix)
            new_xaxis.set_xticks(xaxis_ticks_dt)
            new_xaxis.set_xticklabels(xaxis_labels)
            ytitle = pytplot.data_quants[label].attrs['plot_options']['yaxis_opt']['axis_label']
            new_xaxis.set_xlabel(ytitle)

        fig.subplots_adjust(bottom=0.05+len(var_label)*0.1)

    # add the color bars to any spectra
    for idx, variable in enumerate(variables):
        plot_extras = pytplot.data_quants[variable].attrs['plot_options']['extras']

        if plot_extras.get('spec') is not None:
            spec = plot_extras['spec']
        else:
            spec = False

        if spec:
            if colorbars.get(variable) is None:
                continue

            # add the color bar
            if pseudo_plot_num == 0:
                # there's going to be a second axis, so we need to make sure there's room for it
                second_axis_size = 0.07

            if num_panels == 1:
                this_axis = axes
            else:
                this_axis = axes[idx]

            fig.subplots_adjust(left=0.14, right=0.87-second_axis_size)
            box = this_axis.get_position()
            pad, width = 0.02, 0.02
            cax = fig.add_axes([box.xmax + pad + second_axis_size, box.ymin, width, box.height])
            if colorbars[variable]['axis_font_size'] is not None:
                cax.tick_params(labelsize=colorbars[variable]['axis_font_size'])
            fig.colorbar(colorbars[variable]['im'], cax=cax, label=colorbars[variable]['ztitle'] + '\n ' + colorbars[variable]['zsubtitle'])

    if return_plot_objects:
        return fig, axes
    
    if save_png is not None and save_png != '':
        plt.savefig(save_png + '.png')

    if save_eps is not None and save_eps != '':
        plt.savefig(save_eps + '.eps')

    if save_svg is not None and save_svg != '':
        plt.savefig(save_svg + '.svg')

    if save_pdf is not None and save_pdf != '':
        plt.savefig(save_pdf + '.pdf')

    if display:
        plt.show()

def get_var_label_ticks(var_xr, times):
    out_ticks = []
    for time in times:
        out_ticks.append('{:.2f}'.format(var_xr.interp(coords={'time': time}, kwargs={'fill_value': 'extrapolate', 'bounds_error': False}).values))
    return out_ticks
