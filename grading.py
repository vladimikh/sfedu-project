#!/usr/bin/env python

import copy

import inkex, simpletransform

class GradingEffect(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        
        self.OptionParser.add_option('--in_length', action='store',
                                     type='float', dest='in_length',
                                     help='Length of the detail')

        self.OptionParser.add_option('--in_width', action='store',
                                     type='float', dest='in_width',
                                     help='Width of the detail')

        self.OptionParser.add_option('--in_size', action='store',
                                     type='int', dest='in_size',
                                     help='Input size of the detail')

        self.OptionParser.add_option('--out_min_size', action='store',
                                     type='int', dest='out_min_size', default=36,
                                     help='Output minimal size of the detail')

        self.OptionParser.add_option('--out_max_size', action='store',
                                     type='int', dest='out_max_size', default=46,
                                     help='Output maximal size of the detail')
                
        self.OptionParser.add_option('--hor_dist', action='store', 
                                     type='int', dest='hor_dist', default=100, 
                                     help='Horizontal translation distance')                             

    def effect(self):
          
        #used in cycles
        scale_len_inc = self.options.in_length
        scale_len_dec = self.options.in_length
        scale_width_inc = self.options.in_width
        scale_width_dec = self.options.in_width
        
        #horizontal distance is set by user
        horiz = self.options.hor_dist
        #vertical is just to keep details on the same lines
        vert = (-20/3)*2
        
        if self.selected:
            for id, node in self.selected.iteritems():
                
                #saving original for decreasing cycle
                initial_node = node
                
                #increasing sizes from current
                for n in range(self.options.in_size, self.options.out_max_size):
                    
                    #calculating length factor 
                    scale_len_next = scale_len_inc + 20/3
                    scale_factor_length = scale_len_next / scale_len_inc 
                    scale_len_inc = scale_len_next
                    
                    #calculating width factor 
                    scale_width_next = scale_width_inc + 1
                    scale_factor_width = scale_width_next / scale_width_inc
                    scale_width_inc = scale_width_next
                    
                    #initializing tranformations                 
                   
                    #horizontal transformation
                    str_hor_translation = 'translate(' + str(self.unittouu(str(horiz) + "mm")) + ', ' + str(self.unittouu(str(vert) + "mm"))  + ')' 
                    horiz_translation = simpletransform.parseTransform(str_hor_translation)
                    
                    #length transformation
                    str_scaling_length = 'scale(' + str(scale_factor_length)  +  ')'
                    scaling_length = simpletransform.parseTransform(str_scaling_length)
                    
                    #width transformation
                    str_scaling_width = 'scale(' + str(scale_factor_width)  +  ')'
                    scaling_width = simpletransform.parseTransform(str_scaling_width)
                    
                    #copying previous size and then applying transformation
                    new_node = copy.deepcopy(node)
                                     
                    #changing length
                    simpletransform.applyTransformToNode(scaling_length, new_node)
                    
                    #changing width
                    simpletransform.applyTransformToNode(scaling_width, new_node)
                    
                    #moving horizontally
                    simpletransform.applyTransformToNode(horiz_translation, new_node)

                    #inserting detail in current layer
                    self.current_layer.append(new_node)

                    node = new_node
                                
                #decreasing sizes from current
                for n in range(self.options.out_min_size,self.options.in_size):
                    
                    scale_len_prev = scale_len_dec - 20/3
                    scale_factor_length = scale_len_prev / scale_len_dec
                    scale_len_dec = scale_len_prev
                    
                    scale_width_prev = scale_width_dec - 1
                    scale_factor_width = scale_width_prev / scale_width_dec
                    scale_width_dec = scale_width_prev
                                        
                    str_hor_translation = 'translate(' + str(self.unittouu(str((-1)*horiz) + "mm")) + ', ' + str(self.unittouu(str((-1)*vert) + "mm"))  + ')' 
                    horiz_translation = simpletransform.parseTransform(str_hor_translation)
                    
                    str_scaling_length = 'scale(' + str(scale_factor_length)  +  ')'
                    scaling_length = simpletransform.parseTransform(str_scaling_length)
                    
                    str_scaling_width = 'scale(' + str(scale_factor_width)  +  ')'
                    scaling_width = simpletransform.parseTransform(str_scaling_width)
                    
                    new_node = copy.deepcopy(initial_node)
                                     
                    simpletransform.applyTransformToNode(scaling_length, new_node)
                    
                    simpletransform.applyTransformToNode(scaling_width, new_node)
                                        
                    simpletransform.applyTransformToNode(horiz_translation, new_node)
                    
                    self.current_layer.append(new_node)

                    initial_node = new_node
                                
effect = GradingEffect()
effect.affect()