CREATE USER 'customer'@'localhost' IDENTIFIED BY 'Admin.12345';
use bookstore;

GRANT ALL ON auth_group TO 'customer'@'localhost';
GRANT ALL ON auth_group_permissions TO 'customer'@'localhost';
GRANT ALL ON auth_permissions TO 'customer'@'localhost';
GRANT ALL ON auth_user TO 'customer'@'localhost';
GRANT ALL ON auth_user_groups TO 'customer'@'localhost';
GRANT ALL ON auth_user_user_permissions TO 'customer'@'localhost';
GRANT ALL ON django_admin_log TO 'customer'@'localhost';
GRANT ALL ON django_content_type TO 'customer'@'localhost';
GRANT ALL ON django_migrations TO 'customer'@'localhost';
GRANT ALL ON django_session TO 'customer'@'localhost';

GRANT ALL ON card TO 'customer'@'localhost';
GRANT ALL ON order_item TO 'customer'@'localhost';
GRANT ALL ON `order` TO 'customer'@'localhost';
GRANT ALL ON customer TO 'customer'@'localhost';
GRANT ALL ON payment TO 'customer'@'localhost';
GRANT ALL ON review TO 'customer'@'localhost';

GRANT SELECT ON author TO 'customer'@'localhost';
GRANT SELECT ON book TO 'customer'@'localhost';
GRANT SELECT ON book_author TO 'customer'@'localhost';
GRANT SELECT ON book_image TO 'customer'@'localhost';
GRANT SELECT ON electronic TO 'customer'@'localhost';
GRANT SELECT ON traditional TO 'customer'@'localhost';
GRANT SELECT ON keyword TO 'customer'@'localhost';
GRANT SELECT ON publisher TO 'customer'@'localhost';
GRANT SELECT ON staff TO 'customer'@'localhost';
GRANT SELECT ON store TO 'customer'@'localhost';
GRANT SELECT ON topic TO 'customer'@'localhost';