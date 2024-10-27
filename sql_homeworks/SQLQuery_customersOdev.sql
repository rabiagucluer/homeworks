-- 1. Customers isimlibirveritabanıoluşturunuz
-- OLUSTURULDU MANUEL


-- 2. Customers tablosundanadı‘A’ harfi ile başlayan kişileri çeken sorguyu yazınız

SELECT *
FROM CUSTOMERS
WHERE NAMESURNAME LIKE 'A%'

-- 3. 1990 ve1995 yıllarıarasındadoğanmüşterileriçekiniz. 1990 ve1995 yıllarıdahildir.
SELECT * FROM CUSTOMERS
WHERE BIRTHDATE BETWEEN '1990-01-01' AND '1995-12-31'

--4. İstanbul’da yaşayan kişileri Join kullanarak gOren sorguyu yazınız.

SELECT C.*, CT.CITY 
FROM CUSTOMERS C
INNER JOIN CITIES CT ON CT.CITYID = CT.ID 
WHERE CT.CITY = 'ISTANBUL'

-- 5. İstanbul’da yaşayan kişileri subquery kullanarak getiren sorguyu yazınız.
--1
SELECT *,
(SELECT CITY FROM CITIES WHERE ID=C.CITYID)
 FROM CUSTOMERS C
WHERE (SELECT CITY FROM CITIES WHERE ID =C.CITYID) ='ISTANBUL'
--2
SELECT * FROM CUSTOMERS C
WHERE C.CITYID IN (SELECT ID FROM CITIES WHERE CITY='ISTANBUL')

-- 6. Hangi şehirde kaç müşterimizin olduğu bilgisini getiren sorguyu yazınız.



--7. 10’dan fazla müşterimiz olan şehirleri müşteri sayısı ile birlikte müşteri sayısına göre fazladan aza doğru sıralı şekilde getiriniz. 
--1
SELECT CT.CITY, COUNT(C.ID) AS CUSTOMERCOUNT FROM CUSTOMER C
INNER JOIN CITIES CT ON CT.ID = C.CITYID 
GROUP BY CT.CITY
HAVING COUNT(C.ID) > 10
ORDER BY COUNT(C.ID) DESC

--2
SELECT * , 
(SELECT COUNT (*) FROM CUSTOMERS WHERE CITYID = C.ID)
FROM CITIES C
WHERE (SELECT COUNT(*) FROM CUSTOMERS WHERE CITYID = C.ID) >10

--8. Hangi şehirde kaç erkek, kaç kadın müşterimizin olduğu bilgisini getiren sorguyu yazınız. 
--1
SELECT CT.CITY, C.GENDER, COUNT(C.ID) AS CUSTOMERCOUNT FROM CUSTOMERS
INNER JOIN CITIES CT ON CT.ID = CITYID
GROUP BY CT.CITY, C.GENDER
ORDER BY CT.CITY
--2
SELECT CITY AS SEHIRADI,
(SELECT COUNT(*) FROM CUSTOMERS WHERE CITYID = C.ID) AS MUSTERISAYISI,
(SELECT COUNT(*) FROM CUSTOMERS WHERE CITYID = C.ID AND GENDER='E') AS ERKEKSAYISI,
(SELECT COUNT(*) FROM CUSTOMERS WHERE CITYID = C.ID AND GENDER='K') AS KADINSAYISI
FROM CITIES C

--9. Customers tablosuna yaş grubu için yeni bir alaN ekleyiniz. Bu işlemi hem management studio ile hem de sql kodu il eyapınız. Alanı adı AGEGROUP veri tipiVarchar(50) 

ALTER TABLE CUSTOMERS ADD AGEGROUP VARCHAR(50)

--10. Customers tablosuna eklediğiniz AGEGROUP alanını 20-35 yaş arası,36-45 yaş arası,46-55 yaş arası,55-65 yaş arası ve 65 yaş üstü olarak güncelleyiniz. 

UPDATE CUSTOMERS SET AGEGROUP = '20-35 YAS'
WHERE DATEDIFF (YEAR, BIRTHDATE, GETDATE()) BETWEEN 20 AND 35

UPDATE CUSTOMERS SET AGEGROUP = '36-45 YAS'
WHERE DATEDIFF (YEAR, BIRTHDATE, GETDATE()) BETWEEN 36 AND 45

UPDATE CUSTOMERS SET AGEGROUP = '46-55 YAS'
WHERE DATEDIFF (YEAR, BIRTHDATE, GETDATE()) BETWEEN 46 AND 55

UPDATE CUSTOMERS SET AGEGROUP = '56-65 YAS'
WHERE DATEDIFF (YEAR, BIRTHDATE, GETDATE()) BETWEEN 56 AND 65

UPDATE CUSTOMERS SET AGEGROUP = '65 YAS ÜSTÜ'
WHERE DATEDIFF (YEAR, BIRTHDATE, GETDATE())> 65


--11. İstanbul’da yaşayıp ilçesi ‘Kadıköy’ dışında olanları listeleyiniz.

SELECT * FROM CUSTOMERS C
INNER JOIN CITIES CT ON CT.ID = C.CITYID
INNER JOIN DISTRICTS D ON D.ID= C.DISTRICTID
WHERE CITY= 'ISTANBUL' AND D.DISTRICT <> 'KADIKÖY'


--12. Müşterilerimizin telefon numalarının operatör bilgisini getimek istyoruz. TELNR1 veTELNR2 alanlarının yanına operatör numarasını (532),(505) gibi getirmek istiyoruz. 
-- Bu sorgu için gereken SQL cümlesini yazınız.


SELECT *,
SUBSTRING(TELNR1,2,3) AS OPERATOR1,
SUBSTRING(TELNR2,2,3) AS OPERATOR2
FROM CUSTOMERS



--13. Müşterilerimizin telefon numaralarının operatör bilgisini getirmek istiyoruz. Örneğin telefon numaraları “50” yada “55” ile başlayan “X” operatörü  “54” ile başlayan “Y” operatörü “53” ile başlayan “Z” operatörü olsun. Burada hangi operatörden ne kadar müşterimiz olduğu bilgisini getirecek sorguyu yazınız. 



--14. Her ilde en çok müşteriye sahip olduğumuz ilçeleri müşteri sayısına göre çoktan aza doğru sıralı şekilde şekildeki gibi getirmek için gereken sorguyu yazınız. 

SELECT CT.CITY, D.DISTRICT, COUNT(C.ID) AS CUSTOMERCOUNT FROM CUSTOMERS C
INNER JOIN CITIES CT ON CT.ID = C.CITYID 
INNER JOIN DISTRICTS D ON D.ID= C.DISTRICTID
GROUP BY CT.CITY, D.DISTRICT
ORDER BY CT.CITY, COUNT(C.ID) DESC

--15. Müşterilerin doğum günlerini haftanın günü (Pazartesi, Salı, Çarşamba..) olarak getiren sorguyu yazınız.
SET LANGUAGE TURKISH

SELECT DATENAME(DW, BIRTHDATE), BIRTHDATE,
* FROM CUSTOMERS

SELECT * FROM sys.syslanguages;

