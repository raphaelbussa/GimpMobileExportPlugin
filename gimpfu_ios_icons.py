#! /usr/bin/env python
'''
Created on 2016/01/05

@author: rebus007

This is a Gimp plugin

Actions:
    - You can select a new width for the icon and select the target density.
    - Drawables for other densities will be scaled accordingly

Installation: 
    - Put this file into your gimp plugin directory, ie: ~/.gimp-2.6/plug-ins/gimpfu_ios_icons.py
    - Restart Gimp
    - Run script via Filters/iOS/Write iOS icons...
'''

import gimpfu
import gimp
import os

DEFAULT_OUTPUT_DIR = os.getcwd()
DEFAULT_OUTPUT_EXT = 'png'
DEFAULT_FOLDER_PREFIX = 'drawable'
DEFAULT_TARGET_PREFIX = 'width'

UPSCALE_WARN_MESSAGE = '\nQuality of your application could be seriously affected when using upscaled bitmaps !'

def write_xdpi(img, layer, res_folder, image_basename, target, target_width_height, x_ldpi, x_mdpi, x_hdpi, image_extension):
    '''
    Resize and write images for all android density folders 
    
    @param img: gimp image
    @param layer: gimp layer (or drawable)
    @param res_folder: output directory : basically res folder of your android project 
    @param image_basename: basename of your image, ex: icon
    @param target: new width for your image
    @param target_width_height: fixed misures
    @param target_dpi: reference density for your target width
    @param image_extension: output format
    '''
    
    warnings = list()
    
    gimpfu.pdb.gimp_edit_copy_visible(img); #@UndefinedVariable
    
    dpi_ratios = (('@1x',    1 ,x_ldpi),
                  ('@2x',    2    ,x_mdpi),
                  ('@3x',    3  ,x_hdpi))

    for folder, ratio, export in dpi_ratios:
        if not export: 
            continue

        new_img = gimpfu.pdb.gimp_edit_paste_as_new(); #@UndefinedVariable
        
        target_dp_width = 0
        target_dp_height = 0
    
        if target_width_height == "width":
            resize_ratio = float(target) / new_img.width
            target_dp_width = target
            target_dp_height = round(new_img.height * resize_ratio)

        if target_width_height == "height":
            resize_ratio = float(target) / new_img.height
            target_dp_width = round(new_img.width * resize_ratio)
            target_dp_height = target
        
        # Compute new dimensions for the image
        new_width = target_dp_width * ratio
        new_height = target_dp_height * ratio
        
        target_res_folder = os.path.join(res_folder, 'icon-' + image_basename)
        if (os.path.exists(res_folder) and not os.path.exists(target_res_folder)):
            os.makedirs(target_res_folder)

        target_res_filename = os.path.join(target_res_folder, image_basename + folder + '.' + image_extension)
        
        # Save the new Image
        gimpfu.pdb.gimp_image_scale_full( #@UndefinedVariable
            new_img, new_width, new_height, gimpfu.INTERPOLATION_CUBIC)
        
        gimpfu.pdb.gimp_file_save( #@UndefinedVariable
            new_img, new_img.layers[0], target_res_filename, target_res_filename)
        
        gimpfu.pdb.gimp_image_delete(new_img) #@UndefinedVariable
        
    # Show warning message
    if warnings: 
        warnings.append(UPSCALE_WARN_MESSAGE)
        gimp.message('\n'.join(warnings))

gimpfu.register("python_fu_ios_icons",
                "Write iOS icons for all icon size",
                "Write images for all iOS sizes",
                "rebus007", "Raphael Bussa", "2017",
                "<Image>/Filters/iOS/Write iOS icons...",
                "*", [
                    (gimpfu.PF_DIRNAME, "res-folder",     "Project icons Folder", DEFAULT_OUTPUT_DIR), #os.getcwd()),
                    (gimpfu.PF_STRING, "image-basename", "Image Base Name", 'icon'),
                    (gimpfu.PF_SPINNER, "target", "Target pt", 50, (1, 8000, 2)),
                    (gimpfu.PF_RADIO, "target-width-height", "Fixed misures", DEFAULT_TARGET_PREFIX, (("width", "width"), ("height", "height"))),
                    (gimpfu.PF_BOOL, "x_ldpi",    "  Export 1x",   True),
                    (gimpfu.PF_BOOL, "x_mdpi",    "  Export 2x",   True),
                    (gimpfu.PF_BOOL, "x_hdpi",    "  Export 3x",   True),
                    (gimpfu.PF_RADIO, "image-extension", "Image Format", DEFAULT_OUTPUT_EXT, (("gif", "gif"), ("png", "png"), ("jpg", "jpg"))),
                      ], 
                [], 
                write_xdpi) #, menu, domain, on_query, on_run)

gimpfu.main()
