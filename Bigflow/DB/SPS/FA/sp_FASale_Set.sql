CREATE DEFINER=`developer`@`%` PROCEDURE `sp_FASale_Set`(IN `ls_Action` varchar(32),IN `ls_Type` varchar(32),IN `ls_Sub_Type` varchar(32),
IN `lj_Details` json,IN `lj_Classification` json,IN `ls_Createby` varchar(32),OUT `li_Last_Id` int,OUT `Message` varchar(1024))
sp_FASale_Set:BEGIN
#### Ramesh Nov 30
Declare errno int;
Declare msg varchar(1000);
Declare countRow int;
Declare Query_Insert varchar(9000);
Declare Query_Update varchar(2048);
Declare i int;

DECLARE EXIT HANDLER FOR SQLEXCEPTION,sqlwarning

    BEGIN

     GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
     set Message = concat(errno , msg);
     ROLLBACK;
     END;

			select JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Gid[0]'))) into @Entity_Gid;

             if @Entity_Gid is  null or @Entity_Gid = 0 or @Entity_Gid = '' then
					set Message = 'Entity Gid Is Needed.';
                    leave sp_FASale_Set;
             End if;

 if ls_Type = 'FAASSET_SALE' and ls_Sub_Type = 'SO_HEADER' then
		   ### Product Gid - Custome gid , Rate,Qty. - - It Include the Details Too
           select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Customer_Gid'))) into @Customer_Gid;
           select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Sale_Date'))) into @Sale_Date;

           select JSON_LENGTH(lj_Details,CONCAT('$.PRODUCT')) into @Product_Length;

                           if @Product_Length is null or @Product_Length = 0  then
								set Message = 'Product Data Is Needed.';
                                rollback;
                                leave sp_FASale_Set;
                           End if;
           ### Validations
           if @Customer_Gid is null or @Customer_Gid = 0 then
					set Message = 'Customer Gid Is Needed.';
                    leave sp_FASale_Set;
           End if;

           if @Sale_Date is null or @Sale_Date = '' THEN
           		set Message = 'Asset Sale Date Is Needed.';
           	   leave sp_FASale_Set;
           End if;


           	select ifnull(max(soheader_no),0) into @code1 from gal_trn_tsoheader where date_format(soheader_date,'%Y-%m-%d') = curdate();
			#select @code1;
			call sp_Generatecode_Get('WITH_DATESMALL', 'SLG', '00', @code1, @Message);

	              call sp_Generate_number_get('SO','000',@Message);
                  	select @Message into @ls_no from dual;

				if @ls_no is null or @ls_no = '' then
					set Message = 'Problem In SO Header No Generation.';
                    leave sp_FASale_Set;
                End if;

               #select @ls_no;

                set @Company_GSTno = '33GST';

                set @SO_Header_Amount = 0;
                set @SO_Header_Total = 0;

            set Query_Insert = '';
            set Query_Insert = concat('Insert into gal_trn_tsoheader (soheader_customer_gid,soheader_no,soheader_gstno,soheader_date,soheader_employee_gid,
                                                          Soheader_channel,soheader_status,soheader_amount,soheader_total,entity_gid,
                                                      create_by)
                                              values (''',@Customer_Gid,''',''',@ls_no,''',''',@Company_GSTno,''',''',@Sale_Date,''',1,''F'',''REQUESTED'',''',@SO_Header_Total,''',
                                              ''',@SO_Header_Total,''',''',@Entity_Gid,''',''',ls_Createby,''')
                                                     ');

													set @Insert_query = Query_Insert;
													#SELECT @Insert_query;
													PREPARE stmt FROM @Insert_query;
													EXECUTE stmt;
													set countRow = (select ROW_COUNT());
													DEALLOCATE PREPARE stmt;

                                                    if countRow > 0 then
                                                          set Message = 'SUCCESS';
                                                               select LAST_INSERT_ID() into @SOHeader_Maxgid ;
                                                               set li_Last_Id = @SOHeader_Maxgid;
                                                     else
                                                          set Message = 'FAIL';
                                                          rollback;
                                                          leave sp_FASale_Set;
                                                    End if;

                                               ### Details part.
							set i = 0 ;
                           While i <= @Product_Length -1 Do


										select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.PRODUCT[',i,'].Product_Gid'))) into @Product_Gid;
										#select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.PRODUCT[',i,'].Product_Qty'))) into @Product_Qty;
										select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.PRODUCT[',i,'].Sale_Rate'))) into @Sale_Rate;

                                        if @Product_Gid is null or @Product_Gid = 0 then
												set Message = 'Product Gid Is Needed.';
                                                rollback;
												leave sp_FASale_Set;
										End if;

                                         if @Sale_Rate is null or @Sale_Rate = 0 then
											set Message = 'Sales Rate Is Needed.';
                                            rollback;
											leave sp_FASale_Set;
									   End if;

                                    #### Get The Qty
                                     set @Product_Qty = 0;
										Select count(a.assetsale_gid) into @Product_Qty from fa_trn_tassetsale as a
										inner join fa_tmp_tassetdetails as b on b.assetdetails_id = a.assetsale_assetdetailsid
										where a.assetsale_value = @Sale_Rate and b.assetdetails_productgid = @Product_Gid
										and a.assetsale_isactive = 'Y' and a.assetsale_isremoved = 'N'
										and b.assetdetails_isactive = 'Y' and b.assetdetails_isremoved = 'N'	;

									   if @Product_Qty is null or @Product_Qty = 0 then
											set Message  = 'Product Quantity Is Needed.' ;
                                            rollback;
											leave sp_FASale_Set;
									   End if;

                                         set @Product_Code = 'RT';
                                         set @UOM_Gid = 0;
                                         set @HSN_Code = '65';
                                         set @Sale_Total = @Product_Qty * @Sale_Rate;
                                         set @Sale_Status = 'APPROVED';
                                         set @Sale_Remark = 'RTY';

                                        ### detail Insert
                                        set Query_Insert = '';
                                        set Query_Insert = concat('
											insert into gal_trn_tsodetails (sodetails_soheader_gid,sodetails_product_gid,sodetails_product_code,
											sodetails_uom_gid,sodetails_unitprice,sodetails_qty,sodetails_hsncode,sodetails_amount,
											sodetails_total,sodetails_status,sodetails_remarks,entity_gid,create_by
											)values(''',@SOHeader_Maxgid,''',''',@Product_Gid,''',''',@Product_Code,''',''',@UOM_Gid,''',
                                              ''',@Sale_Rate,''',''',@Product_Qty,''',''',@HSN_Code,''',''',@Sale_Total,''',
                                             ''',@Sale_Total,''',''',@Sale_Status,''',''',@Sale_Remark,''',''',@Entity_Gid,''',''',ls_Createby,'''
                                             )');

                                            		set @Insert_query = '';
                                                   set @Insert_query = Query_Insert;
													#SELECT @Insert_query;
													PREPARE stmt FROM @Insert_query;
													EXECUTE stmt;
													set countRow = (select ROW_COUNT());
													DEALLOCATE PREPARE stmt;

                                                    if countRow > 0 then
                                                          set Message = 'SUCCESS';
                                                               #select LAST_INSERT_ID() into @SOHeader_Maxgid ;
                                                     else
                                                          set Message = 'FAIL';
                                                          rollback;
                                                          leave sp_FASale_Set;
                                                    End if;


                                 set i = i+1;
                           End while;

  elseif ls_Type = 'SALE_MAKER' and ls_Sub_Type = 'SALE_HEADER' then
               #### To Save The asset Sale only in Asset Tables - Not So header Table.
       select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.Customer_Gid')) into @Customer_Gid;
       select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.Branch_Gid')) into @Branch_Gid;
       select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.Sale_Date')) into @Sale_Date;
       select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.Status')) into @ls_Status;
       select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.Remarks')) into @Remarks;
       ### Validation is Needed

          set Query_Insert = '';
          set Query_Insert = concat('Insert into fa_trn_tassetsaleheader(assetsaleheader_customergid,assetsaleheader_salebranchgid,assetsaleheader_saledate,
			assetsaleheader_saletotalamount,assetsaleheader_invoiceheadergid,assetsaleheader_status,assetsaleheader_remarks,entity_gid,create_by)
            values (''',@Customer_Gid,''',''',@Branch_Gid,''',''',@Sale_Date,''',0,0,''',@ls_Status,''',''',@Remarks,''',''',@Entity_Gid,''',''',ls_Createby,''')'
            );

												set @Insert_query = Query_Insert;
													#SELECT @Insert_query;
													PREPARE stmt FROM @Insert_query;
													EXECUTE stmt;
													set countRow = (select ROW_COUNT());
													DEALLOCATE PREPARE stmt;

                                                    if countRow > 0 then
                                                          set Message = 'SUCCESS';
                                                               select LAST_INSERT_ID() into @AssetSaleH_Maxgid ;
                                                               set li_Last_Id = @AssetSaleH_Maxgid;
                                                     else
                                                          set Message = 'FAIL';
                                                          leave sp_FASale_Set;
                                                    End if;


													call sp_Trans_Set('Insert','FA_SALE',@AssetSaleH_Maxgid,'PENDING','G',
																	  'MAKER',@Remarks,@Entity_Gid,ls_Createby,@message);
													select @message into @tran;
													#select @message; #remove it
													if @tran <>0 or @tran <> '' then
															set Message = 'SUCCESS';
													else
															set Message = 'FAIL in tran';
															leave sp_FASale_Set;
													end if;

 elseif ls_Type = 'SALE_MAKER' and ls_Sub_Type = 'SALE_DETAIL' then
     ### To Save The Asset Detail table
     	 select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.SaleHeader_Gid')) into @SaleHeader_Gid;
	     select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.Sale_Date')) into @Sale_Date;
	   	 select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.Sale_Status')) into @Sale_Status;
   		 select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.Sale_Reason')) into @Sale_Reason;
	 	 select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.Sale_Rate')) into @Sale_Rate;
	 	 select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.Assetdetail_Gids')) into @Assetdetail_Gids;


	# select @SaleHeader_Gid,@Sale_Date,@Sale_Status,@Sale_Reason,@Sale_Rate,@Entity_Gid,ls_Createby,@Assetdetail_Gids;
	 set Query_Insert = '';
	 set Query_Insert = concat('insert into fa_trn_tassetsale (assetsale_assetsaleheadergid,assetsale_assetdetailsid,assetsale_date,
		assetsale_status,assetsale_reason,assetsale_customer,assetsale_value,assetsale_invoiceheadergid,entity_gid,create_by)
	 	(select ''',@SaleHeader_Gid,''',assetdetails_id,''',@Sale_Date,''',''',@Sale_Status,''',''',@Sale_Reason,''',
     	''XXX'',''',@Sale_Rate,''',0,''',@Entity_Gid,''',''',ls_Createby,''' from fa_trn_tassetdetails
		where assetdetails_gid in (',@Assetdetail_Gids,')
 		)');

						set @Insert_query = '';
 						set @Insert_query = Query_Insert;
						#SELECT @Insert_query;
						PREPARE stmt FROM @Insert_query;
						EXECUTE stmt;
						set countRow = (select ROW_COUNT());
						DEALLOCATE PREPARE stmt;

                        if countRow > 0 then
                              set Message = 'SUCCESS';
                         else
                              set Message = 'FAIL';
                              leave sp_FASale_Set;
                        End if;



elseif ls_Type = 'INVOICE_HEADER_MAKER' and ls_Sub_Type = 'INVOICE_HEADER' then
     ### To Save The Asset Detail table

              select JSON_LENGTH(lj_Details,CONCAT('$.PRODUCT[0]')) into @Product_Length;
			 #select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Product_Qty'))) into @InvoiceDetails_QTY;
			  select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Customer_Gid'))) into @Customer_Gid;

                        set i = 0 ;
                           While i < @Product_Length Do

						select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.PRODUCT[',i,'].inv_pdct_gid'))) into @Inv_Product_Gid;
						select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.PRODUCT[',i,'].Product_Qty'))) into @InvoiceDetails_QTY;
						select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.PRODUCT[',i,'].inv_sale_rate'))) into @Inv_Sale_Rate;


                            set @Invoice_Gid=12;
                            set @Campaign_Gid=13;
                            set @Product_Code='PRcd123';
							set @UOM_Gid=99;
						    set @Unit_Price=2000;
							set @InvoiceDetails_HSN_Code='HSNCD123';
							set	@Dealer_Price=3000;
                            set @NRP_price=4000;
							set @InvoiceDetails_CGST=60.00;
                            set @InvoiceDetails_SGST=70.00;
							set	@InvoiceDetails_IGST=45.00;
							set @Tax_Amount=70;
							set	@Discount=40;
							set	@Total=@InvoiceDetails_QTY*@Inv_Sale_Rate;




	 set Query_Insert = '';
	 set Query_Insert = concat('INSERT INTO gal_trn_tinvoicedetails
										(invoicedetails_invoice_gid,invoicedetails_campaign_gid,invoicedetails_product_gid,
                                        invoicedetails_product_code,invoicedetails_uom_gid,invoicedetails_unitprice, invoicedetails_qty,
                                        invoicedetails_hsncode,invoicedetails_dealerprice, invoicedetails_nrpprice,
                                        invoicedetails_cgst,invoicedetails_sgst, invoicedetails_igst, invoicedetails_taxamount,
                                        invoicedetails_discount, invoicedetails_total,entity_gid, create_by )
								 VALUES(',@Invoice_Gid,',',@Campaign_Gid,',',@Inv_Product_Gid,',''',@Product_Code,''',
										',@UOM_Gid,',',@Unit_Price,',',@InvoiceDetails_QTY,',''',@InvoiceDetails_HSN_Code,''',
                                        ',@Dealer_Price,',',@NRP_price,',',@InvoiceDetails_CGST,',',@InvoiceDetails_SGST,',
                                        ',@InvoiceDetails_IGST,',',@Tax_Amount,',',@Discount,',',@Total,',
                                        ',@Entity_Gid,',',ls_Createby,')
								');

						set @Insert_query = '';
 						set @Insert_query = Query_Insert;
						#SELECT @Insert_query,1;
						PREPARE stmt FROM @Insert_query;
						EXECUTE stmt;
						set countRow = (select ROW_COUNT());
						DEALLOCATE PREPARE stmt;

                        if countRow > 0 then
                              set Message = 'SUCCESS';
                         else
                              set Message = 'FAIL';
                              leave sp_FASale_Set;
                        End if;

						set i = i+1;
				End while;



			#select ifnull(max(invoiceheader_no),0) into @code1 from gal_trn_tinvoiceheader ;
			select ifnull(invoiceheader_no,0) into @code1 from gal_trn_tinvoiceheader order by invoiceheader_gid desc limit 1 ;

			#select @code1;

	                call sp_Generatecode_Get('WITHOUT_DATE', 'V', '000', @code1, @Message);
                  	select @Message into @InvoiceHeader_No from dual;
                  	#select  @InvoiceHeader_No;

				#select @ls_no;

                        #set @Customer_Gid=2;
                        #set @InvoiceHeader_No=28;#Auto_generator
                        set @InvoiceHeader_GST_No='GST003';
                        set @InvoiceHeader_Date='2019-05-12';
                        set @Employee_Gid=13;
                        set @InvoiceHeader_Channel='INVH003';
                        set @Remarks='Test_Remarks';
                        set @Invoice_Status='NEW';
                        set @Amount=5000;
                        set @Discount=1000;
                        set @Tax_Amount=50;
                        set @Inv_Total=150;
                        set @OutStanding=17.50;
                        set @Customer_GST_No=173;
                        set @Despatch_Gid=14;
                        set @IsPrint=12;
                        set @EntityDetails_Gid=2;
                        set @Branch_Gid=7;

				#select @Customer_Gid,@InvoiceHeader_No,@InvoiceHeader_GST_No,@InvoiceHeader_Date,@Employee_Gid,
    		    #@InvoiceHeader_Channel,@Remarks,ls_Createby,@Invoice_Status,@Amount,@Discount,@Tax_Amount,
                # @Inv_Total,@OutStanding,@Customer_GST_No,@Despatch_Gid,@IsPrint,@EntityDetails_Gid,@Branch_Gid;

	 set Query_Insert = '';
	 set Query_Insert = concat('INSERT INTO gal_trn_tinvoiceheader
										(invoiceheader_customer_gid, invoiceheader_no,invoiceheader_gstno,
										invoiceheader_date, invoiceheader_employee_gid,invoiceheader_channel,
										invoiceheader_remarks, invoiceheader_status,invoiceheader_amount,
										invoiceheader_discount, invoiceheader_taxamount,invoiceheader_total,
										invoiceheader_outstanding, invoiceheader_customergstno,invoiceheader_despatch_gid,
										invoiceheader_isprint,  entity_gid, entitydetails_gid,branch_gid,create_by)
								 VALUES(',@Customer_Gid,',''',@InvoiceHeader_No,''',''',@InvoiceHeader_GST_No,''',
										''',@InvoiceHeader_Date,''',',@Employee_Gid,',''',@InvoiceHeader_Channel,''',
										''',@Remarks,''',''',@Invoice_Status,''',',@Amount,',',@Discount,',',@Tax_Amount,',
										',@Inv_Total,',',@OutStanding,',',@Customer_GST_No,',',@Despatch_Gid,',',@IsPrint,',
										',@Entity_Gid,',',@EntityDetails_Gid,',',@Branch_Gid,',',ls_Createby,')
								');

						set @Insert_query = '';
 						set @Insert_query = Query_Insert;
						#SELECT @Insert_query,2;
						PREPARE stmt FROM @Insert_query;
						EXECUTE stmt;
						set countRow = (select ROW_COUNT());
						DEALLOCATE PREPARE stmt;

                        if countRow > 0 then
                              set Message = 'SUCCESS';
                         else
                              set Message = 'FAIL';
                              leave sp_FASale_Set;
                        End if;


elseif ls_Type = 'SO_INVOICE_MAKER' and ls_Sub_Type = 'SO_INVOICE' then
     ### To Save The Asset Detail table

			select JSON_LENGTH(lj_Details, CONCAT('$')) into @lj_Details_JSON_COUNT;

             if  @lj_Details_JSON_COUNT = 0 or @lj_Details_JSON_COUNT is  null or @lj_Details_JSON_COUNT = '' then
					set Message = 'No Data In lj_Details JSON';
                    leave sp_FASale_Set;
             End if;

     	select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.SO_Header_Gid')) into @SO_Header_Gid;
	    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.SO_Details_Gid')) into @SO_Details_Gid;
	   	select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.Invoice_header_Gid')) into @Invoice_header_Gid;


        if @SO_Header_Gid='' or @SO_Header_Gid is null then
			set Message='SO_Header Gid Is Not Given';
        end if;

				#select @Customer_Gid,@InvoiceHeader_No,@InvoiceHeader_GST_No,@InvoiceHeader_Date,@Employee_Gid,
    			#@InvoiceHeader_Channel,Remarks,ls_Createby,@Invoice_Status,@Amount,@Discount,@Tax_Amount,
                #@Total,@OutStanding,@Customer_GST_No,@Despatch_Gid,@IsPrint,@EntityDetails_Gid,@Branch_Gid;
	 set Query_Insert = '';
	 set Query_Insert = concat('INSERT INTO gal_map_tsoinv
										(soinv_soheader_gid,soinv_sodetails_gid,
                                        soinv_invoiceheader_gid,entity_gid,create_by)
								 VALUES(',@SO_Header_Gid,',''',@SO_Details_Gid,''',
                                        ''',@Invoice_header_Gid,''',',@Entity_Gid,',',ls_Createby,')
								');

						set @Insert_query = '';
 						set @Insert_query = Query_Insert;
						#SELECT @Insert_query;
						PREPARE stmt FROM @Insert_query;
						EXECUTE stmt;
						set countRow = (select ROW_COUNT());
						DEALLOCATE PREPARE stmt;

                        if countRow > 0 then
                              set Message = 'SUCCESS';
                         else
                              set Message = 'FAIL';
                              leave sp_FASale_Set;
                        End if;

 End if;


END