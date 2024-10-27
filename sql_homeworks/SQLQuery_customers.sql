-- Soru 1:  Customers isimli bir veritabanı ve verilen veri setindeki değişkenleri içerecek FLO isimli bir tablo oluşturunuz.
-- OLusturuldu

SELECT * FROM flo_customer


--soru 2: Kaç farklı müşterinin alışveriş yaptığını gösterecek sorguyu yazınız.

SELECT COUNT(DISTINCT master_id) AS unique_customers

FROM flo_customer;

--soru 3: Toplam yapılan alışveriş sayısı ve ciroyu getirecek sorguyu yazınız.

SELECT
	SUM(order_num_total_ever_online + order_num_total_ever_offline) AS total_orders,
	SUM(customer_value_total_ever_offline + customer_value_total_ever_online ) AS total_value
FROM flo_customer;

--soru 4: Alışveriş başına ortalama ciroyu getirecek sorguyu yazınız.

SELECT
	
	SUM(customer_value_total_ever_offline + customer_value_total_ever_online )/
	SUM(order_num_total_ever_online + order_num_total_ever_offline) AS average_per_order
FROM flo_customer;

--soru 5: En son alışveriş yapılan kanal (last_order_channel) üzerinden yapılan alışverişlerin toplam ciro ve alışveriş sayılarını
--getirecek sorguyu yazınız. 

SELECT
    last_order_channel,
	SUM(order_num_total_ever_online + order_num_total_ever_offline) AS baslik,
	SUM(order_num_total_ever_online + order_num_total_ever_offline ) AS total_orders
FROM flo_customer 
GROUP BY last_order_channel;


--soru 6: Store type kırılımında elde edilen toplam ciroyu getiren sorguyu yazınız.

SELECT
    store_type,
	SUM(order_num_total_ever_online + order_num_total_ever_offline) AS total_value
FROM flo_customer
GROUP BY store_type;

--soru 7: Yıl kırılımında alışveriş sayılarını getirecek sorguyu yazınız (Yıl olarak müşterinin ilk alışveriş tarihi (first_order_date) yılını
-- baz alınız)

SELECT
    YEAR(first_order_date) AS order_year,
	SUM(order_num_total_ever_online + order_num_total_ever_offline) AS total_orders

FROM flo_customer
GROUP BY YEAR(first_order_date)
ORDER BY order_year;

--soru 8: En son alışveriş yapılan kanal kırılımında alışveriş başına ortalama ciroyu hesaplayacak sorguyu yazınız. 

SELECT
    last_order_channel,
	round ( SUM(customer_value_total_ever_offline + customer_value_total_ever_online),2) AS total_ciro,
	round ( SUM(customer_value_total_ever_offline + customer_value_total_ever_online) /
	SUM(order_num_total_ever_online + order_num_total_ever_offline ) ,2) AS average_per_order
FROM flo_customer 
GROUP BY last_order_channel;

--soru 9: Son 12 ayda en çok ilgi gören kategoriyi getiren sorguyu yazınız..

SELECT 
     interested_in_categories_12,
	 COUNT(*) AS interest_count
FROM flo_customer

GROUP BY interested_in_categories_12
ORDER BY interest_count DESC;

--soru 10: En çok tercih edilen store_type bilgisini getiren sorguyu yazınız.

SELECT top 10
    store_type,
	COUNT(*) AS preference_count
FROM flo_customer
GROUP BY store_type
ORDER BY preference_count DESC;

-- Soru 11:  En son alışveriş yapılan kanal (last_order_channel) bazında, en çok ilgi gören kategoriyi ve bu kategoriden ne kadarlık
-- alışveriş yapıldığını getiren sorguyu yazınız.

SELECT
    last_order_channel,
	(SELECT 
     interested_in_categories_12,
	 COUNT(*) AS interest_count
	FROM flo_customer
	GROUP BY interested_in_categories_12
	ORDER BY interest_count DESC)
FROM flo_customer


-- Soru 12: En çok alışveriş yapan kişinin ID’ sini getiren sorguyu yazınız. 


-- Soru 13: En çok alışveriş yapan kişinin alışveriş başına ortalama cirosunu ve alışveriş yapma gün ortalamasını (alışveriş sıklığını)
-- getiren sorguyu yazınız.

-- Soru 14: En çok alışveriş yapan (ciro bazında) ilk 100 kişinin alışveriş yapma gün ortalamasını (alışveriş sıklığını) getiren sorguyu
-- yazınız

-- Soru 15: En son alışveriş yapılan kanal (last_order_channel) kırılımında en çok alışveriş yapan müşteriyi getiren sorguyu yazınız. 

-- Soru 16: En son alışveriş yapan kişinin ID’ sini getiren sorguyu yazınız. (Max son tarihte birden fazla alışveriş yapan ID bulunmakta.
-- Bunları da getiriniz.) 
