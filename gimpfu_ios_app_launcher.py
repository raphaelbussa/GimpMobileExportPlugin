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

UPSCALE_WARN_MESSAGE = '\nQuality of your application could be seriously affected when using upscaled bitmaps !'

def write_xdpi(img, layer, res_folder, image_basename, image_extension):
    '''
    Resize and write images for all android density folders 
    
    @param img: gimp image
    @param layer: gimp layer (or drawable)
    @param res_folder: output directory : basically res folder of your android project 
    @param image_basename: basename of your image, ex: icon
    @param target_width: new width for your image
    @param target_dpi: reference density for your target width
    @param image_extension: output format
    '''
    
    warnings = list()
    
    gimpfu.pdb.gimp_edit_copy_visible(img); #@UndefinedVariable
    
    dpi_ratios = (('iPhone-20@1x', 20 ),
                  ('iPhone-20@2x', 40 ),
                  ('iPhone-20@3x', 60 ),
                  ('iPhone-29@1x', 29 ),
                  ('iPhone-29@2x', 58 ),
                  ('iPhone-29@3x', 87 ),
                  ('iPhone-40@1x', 40 ),
                  ('iPhone-40@2x', 80 ),
                  ('iPhone-40@3x', 120 ),
                  ('iPhone-60@1x', 60 ),
                  ('iPhone-60@2x', 120 ),
                  ('iPhone-60@3x', 180 ),
                  ('iPad-20@1x', 20 ),
                  ('iPad-20@2x', 40 ),
                  ('iPad-20@3x', 60 ),
                  ('iPad-29@1x', 29 ),
                  ('iPad-29@2x', 58 ),
                  ('iPad-29@3x', 87 ),
                  ('iPad-40@1x', 40 ),
                  ('iPad-40@2x', 80 ),
                  ('iPad-40@3x', 120 ),
                  ('iPad-76@1x', 76 ),
                  ('iPad-76@2x', 152 ),
                  ('iPad-76@3x', 228 ),
                  ('iPad-83.5@1x', 83.5 ),
                  ('iPad-83.5@2x', 167 ),
                  ('iPad-83.5@3x', 250.5 ),
                  ('iTunesArtwork@1x', 512 ),
                  ('iTunesArtwork@2x', 1024 ),
                  ('iTunesArtwork@3x', 1536 ))

    for folder, ratio in dpi_ratios:

        new_img = gimpfu.pdb.gimp_edit_paste_as_new(); #@UndefinedVariable
        
        # Compute new dimensions for the image
        new_width = ratio
        new_height = ratio
        
        target_res_folder = os.path.join(res_folder, 'app-icon-' + image_basename)
        if (os.path.exists(res_folder) and not os.path.exists(target_res_folder)):
            os.makedirs(target_res_folder)

        target_res_filename = os.path.join(target_res_folder, "Icon-" + folder + '.' + image_extension)
        
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

gimpfu.register("python_fu_ios_app_launcher",
                "Write iOS icons launcher for all icon size",
                "Write icons launcher for all iOS sizes",
                "rebus007", "Raphael Bussa", "2016",
                "<Image>/Filters/iOS/Write iOS icons launcher...",
                "*", [
                    (gimpfu.PF_DIRNAME, "res-folder",     "Project icons Folder", DEFAULT_OUTPUT_DIR), #os.getcwd()),
                    (gimpfu.PF_STRING, "image-basename", "Project Name", 'icon'),
                    (gimpfu.PF_RADIO, "image-extension", "Image Format", DEFAULT_OUTPUT_EXT, (("gif", "gif"), ("png", "png"), ("jpg", "jpg"))),
                      ], 
                [], 
                write_xdpi) #, menu, domain, on_query, on_run)

gimpfu.main()
