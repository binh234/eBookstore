# Create role for customer
DROP ROLE IF EXISTS 'bookstore_customer';
CREATE ROLE 'bookstore_customer';
use bookstore;

GRANT SELECT, INSERT, UPDATE, DELETE ON auth_group TO 'bookstore_customer';
GRANT SELECT, INSERT, UPDATE, DELETE ON auth_group_permissions TO 'bookstore_customer';
GRANT SELECT, INSERT, UPDATE, DELETE ON auth_permission TO 'bookstore_customer';
GRANT SELECT, INSERT, UPDATE, DELETE ON auth_user TO 'bookstore_customer';
GRANT SELECT, INSERT, UPDATE, DELETE ON auth_user_groups TO 'bookstore_customer';
GRANT SELECT, INSERT, UPDATE, DELETE ON auth_user_user_permissions TO 'bookstore_customer';
GRANT SELECT, INSERT, UPDATE, DELETE ON django_admin_log TO 'bookstore_customer';
GRANT SELECT, INSERT, UPDATE, DELETE ON django_content_type TO 'bookstore_customer';
GRANT SELECT, INSERT, UPDATE, DELETE ON django_migrations TO 'bookstore_customer';
GRANT SELECT, INSERT, UPDATE, DELETE ON django_session TO 'bookstore_customer';

GRANT SELECT, INSERT, UPDATE, DELETE ON card TO 'bookstore_customer';
GRANT SELECT, INSERT, UPDATE, DELETE ON order_item TO 'bookstore_customer';
GRANT SELECT, INSERT, UPDATE, DELETE ON `order` TO 'bookstore_customer';
GRANT SELECT, INSERT, UPDATE, DELETE ON customer TO 'bookstore_customer';
GRANT SELECT, INSERT, UPDATE, DELETE ON payment TO 'bookstore_customer';
GRANT SELECT, INSERT, UPDATE, DELETE ON review TO 'bookstore_customer';

GRANT SELECT ON author TO 'bookstore_customer';
GRANT SELECT ON book TO 'bookstore_customer';
GRANT SELECT ON book_author TO 'bookstore_customer';
GRANT SELECT ON book_image TO 'bookstore_customer';
GRANT SELECT ON electronic TO 'bookstore_customer';
GRANT SELECT ON traditional TO 'bookstore_customer';
GRANT SELECT ON keyword TO 'bookstore_customer';
GRANT SELECT ON publisher TO 'bookstore_customer';
GRANT SELECT ON staff TO 'bookstore_customer';
GRANT SELECT ON store TO 'bookstore_customer';
GRANT SELECT ON topic TO 'bookstore_customer';





# Create role for staff
DROP ROLE IF EXISTS 'bookstore_staff';
CREATE ROLE 'bookstore_staff';
USE bookstore;

GRANT SELECT, INSERT, UPDATE, DELETE ON auth_group TO 'bookstore_staff';
GRANT SELECT, INSERT, UPDATE, DELETE ON auth_group_permissions TO 'bookstore_staff';
GRANT SELECT, INSERT, UPDATE, DELETE ON auth_permission TO 'bookstore_staff';
GRANT SELECT, INSERT, UPDATE, DELETE ON auth_user TO 'bookstore_staff';
GRANT SELECT, INSERT, UPDATE, DELETE ON auth_user_groups TO 'bookstore_staff';
GRANT SELECT, INSERT, UPDATE, DELETE ON auth_user_user_permissions TO 'bookstore_staff';
GRANT SELECT, INSERT, UPDATE, DELETE ON django_admin_log TO 'bookstore_staff';
GRANT SELECT, INSERT, UPDATE, DELETE ON django_content_type TO 'bookstore_staff';
GRANT SELECT, INSERT, UPDATE, DELETE ON django_migrations TO 'bookstore_staff';
GRANT SELECT, INSERT, UPDATE, DELETE ON django_session TO 'bookstore_staff';

GRANT SELECT, INSERT, UPDATE, DELETE ON order_item TO 'bookstore_staff';
GRANT SELECT, INSERT, UPDATE, DELETE ON `order` TO 'bookstore_staff';
GRANT SELECT, INSERT, UPDATE, DELETE ON payment TO 'bookstore_staff';
GRANT SELECT, INSERT, UPDATE, DELETE ON author TO 'bookstore_staff';
GRANT SELECT, INSERT, UPDATE, DELETE ON book TO 'bookstore_staff';
GRANT SELECT, INSERT, UPDATE, DELETE ON book_author TO 'bookstore_staff';
GRANT SELECT, INSERT, UPDATE, DELETE ON book_image TO 'bookstore_staff';
GRANT SELECT, INSERT, UPDATE, DELETE ON electronic TO 'bookstore_staff';
GRANT SELECT, INSERT, UPDATE, DELETE ON traditional TO 'bookstore_staff';
GRANT SELECT, INSERT, UPDATE, DELETE ON keyword TO 'bookstore_staff';
GRANT SELECT, INSERT, UPDATE, DELETE ON topic TO 'bookstore_staff';
GRANT SELECT, INSERT, UPDATE, DELETE ON publisher TO 'bookstore_staff';
GRANT SELECT, INSERT, UPDATE, DELETE ON staff TO 'bookstore_staff';
GRANT SELECT, INSERT, UPDATE, DELETE ON store TO 'bookstore_staff';
GRANT SELECT, INSERT, UPDATE, DELETE ON import_history TO 'bookstore_staff';
GRANT SELECT, INSERT, UPDATE, DELETE ON export_history TO 'bookstore_staff';

GRANT SELECT ON customer TO 'bookstore_staff';
GRANT SELECT ON card TO 'bookstore_staff';
GRANT SELECT ON review TO 'bookstore_staff';




# Grant role for customer and staff
DROP USER IF EXISTS 'customer'@'localhost';
DROP USER IF EXISTS 'staff'@'localhost';
CREATE USER 'customer'@'localhost' IDENTIFIED BY 'Admin.12345';
CREATE USER 'staff'@'localhost' IDENTIFIED BY 'Admin.12345';
USE bookstore;

GRANT 'bookstore_customer' TO 'customer'@'localhost';
GRANT 'bookstore_staff' TO 'staff'@'localhost';

SET DEFAULT ROLE ALL TO
  'customer'@'localhost',
  'staff'@'localhost';