css-plot-rawsignal
css-overview-gui; initialize from current folder (Raw/micro/ncs) and save the actions to file (see actions menu). This will generate do_extract.txt file that should contain all ncs files in the folder.
css-extract --jobs do_extract.txt
css-plot-extracted
css-find-concurrent
css-mask-artifacts
# Repeat step 2: open css-overview-gui; initialize from current folder (Raw/micro/ncs) and save the actions to file (see actions menu). This will generate do_sort_pos.txt file used in the next step (you could repeat this step also for negative spikes, by clicking in the gui on sort-neg before saving the actions).
css-prepare-sorting --jobs do_sort_pos.txt
css-cluster --jobs sort_pos_yl2.txt
css-combine --jobs sort_pos_yl2.txt
css-plot-sorted --label sort_pos_yl2
#12. (fine tuning) css-gui and css-overview-gui
