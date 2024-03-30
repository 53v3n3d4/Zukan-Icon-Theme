<p>This is going to be ignored by PHP and displayed by the browser.</p>
<?php echo 'While this is going to be parsed.'; ?>
<p>This will also be ignored by PHP and displayed by the browser.</p>

<?php if ($expression == true): ?>
This will show if the expression is true.
<?php else: ?>
Otherwise this will show.
<?php endif; ?>

<?php
$var = NULL;       
?>

<?php
$a = 1234; // decimal number
$a = 0123; // octal number (equivalent to 83 decimal)
$a = 0o123; // octal number (as of PHP 8.1.0)
$a = 0x1A; // hexadecimal number (equivalent to 26 decimal)
$a = 0b11111111; // binary number (equivalent to 255 decimal)
$a = 1_234_567; // decimal number (as of PHP 7.4.0)
?>

<?php
class foo
{
    function do_foo()
    {
        echo "Doing foo."; 
    }
}

$bar = new foo;
$bar->do_foo();
?>

<?php
// Our closure
$double = function($a) {
    return $a * 2;
};

// This is our range of numbers
$numbers = range(1, 5);

// Use the closure as a callback here to
// double the size of each element in our
// range
$new_numbers = array_map($double, $numbers);

print implode(' ', $new_numbers);
?>

<?php

// Valid constant names
define("FOO",     "something");
define("FOO2",    "something else");
define("FOO_BAR", "something more");

// Invalid constant names
define("2FOO",    "something");

// This is valid, but should be avoided:
// PHP may one day provide a magical constant
// that will break your script
define("__FOO__", "something"); 

?>

<?php namespace fub;
  include 'file1.php';
  include 'file2.php';
  include 'file3.php';
  use foo as feline;
  use bar as canine;
  use animate;
  echo \feline\Cat::says(), "<br />\n";
  echo \canine\Dog::says(), "<br />\n";
  echo \animate\Animal::breathes(), "<br />\n";  ?>

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