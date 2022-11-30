<?php

function theme_enqueue_styles(){

    $parent_style = 'parent-style';

    wp_enqueue_style( $parent_style, get_template_directory_uri() . '/style.css' );
    wp_enqueue_style( 'child-style', get_stylesheet_directory_uri() . '/style.css', array( $parent_style )
    );

}

add_action( 'wp_enqueue_scripts', 'theme_enqueue_styles' );

if( !isset( $content_width ) )
    $content_width = 1200;
// remove click image
add_filter( 'the_content', 'attachment_image_link_remove_filter' );

function attachment_image_link_remove_filter( $content ){
    $content = preg_replace(
        array( '{<a(.*?)(wp-att|wp-content\/uploads)[^>]*><img}',
        '{ wp-image-[0-9]*" /></a>}' ), array( '<img', '" />' ), $content
    );
    return $content;

}

/**
 * Wp-activate.php error 500 Multisite not activating user
 */
// not working
add_action ('activate_header', 'load_site_specific_plugin') ;

function
load_site_specific_plugin ()
{
    if (wp_installing ()) {
        require_once (WP_PLUGIN_DIR . '/woocommerce') ;
        }

    return ;
}


/**
 *
 * WooCommerce
 * Remove cart if empty
 *
 */
// Remove cart if empty
add_action( 'wp_print_footer_scripts', 'rm_empty_card' );

function rm_empty_card(){
    if ( WC()->cart->get_cart_contents_count() == 0 ) {
        ?><style>
            #woocommerce_widget_cart-2 {display: none;}
        </style><?php

    }
}

?>