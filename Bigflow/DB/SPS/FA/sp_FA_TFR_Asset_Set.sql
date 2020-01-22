CREATE DEFINER=`developer`@`%` PROCEDURE `sp_FA_TFR_Asset_Set`(IN `ls_Action` varchar(32),
IN `ls_Type` varchar(32),IN `ls_Sub_Type` varchar(32),IN `lj_Details` json,IN `lj_Classification` json,
IN `ls_Createby` varchar(32),OUT `Message` varchar(1024))
sp_FA_TFR_Asset_Set:BEGIN

#### Bala Oct 16 2019
### Ramesh Edit Nov 7 2019
Declare errno int;
Declare msg varchar(1000);
Declare countRow int;
Declare Query_Update varchar(9000);
Declare Query_Insert varchar(9000);

DECLARE EXIT HANDLER FOR SQLEXCEPTION,sqlwarning

	 BEGIN
		GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
		set Message = concat(errno , msg);
		ROLLBACK;
     END;

	select JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Gid[0]'))) into @Entity_Gid;

             if @Entity_Gid is  null or @Entity_Gid = 0 or @Entity_Gid = '' then
					set Message = 'Entity Gid Is Needed.';
                    leave sp_FA_TFR_Asset_Set;
             End if;

if ls_Type = 'TFR_MAKER' and  ls_Sub_Type = 'TRAN' then
      if ls_Action = 'INSERT' then

                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_TFR_To'))) into @Asset_TFR_To;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_TFR_Reason'))) into @Asset_TFR_Reason;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_Detail_Gids'))) into @Asset_Detail_Gids;
                #select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.New_Asset_Detail_Gids'))) into @New_Asset_Detail_Gids;

					if @Asset_TFR_To is null or @Asset_TFR_To = '' then
						set Message = 'Asset_TFR_To Is Needed.';
						leave sp_FA_TFR_Asset_Set;
					End if;

					if @Asset_TFR_Reason is null or @Asset_TFR_Reason = '' then
						set Message = 'Asset Transfer Reason Is Needed.';
						leave sp_FA_TFR_Asset_Set;
					End if;

					if @Asset_Detail_Gids is null or @Asset_Detail_Gids = '' then
						set Message = 'Asset_Detail_Gids Is Needed.';
						leave sp_FA_TFR_Asset_Set;
					End if;

                    set @ls_Status = 'IN_ACTIVE';
                    set @ls_Request_For = 'TRANSFER';
                    set @ls_Request_Status = 'SUBMITTED';
                    set @New_Asset_Id = '';
                    select max(assetdetails_id) + 10 into @New_Asset_Id from fa_tmp_tassetdetails;
                    ##### Creation Of New Asset
                    set Query_Insert = '';
						 set Query_Insert = concat('
						  INSERT INTO fa_tmp_tassetdetails
							(assetdetails_id,assetdetails_qty,assetdetails_barcode,assetdetails_date,assetdetails_assetgroupid,assetdetails_assetcatgid,assetdetails_cat,
							assetdetails_subcat,assetdetails_productgid,assetdetails_value,assetdetails_cost,assetdetails_description,assetdetails_capdate,assetdetails_source,
                            assetdetails_status,assetdetails_requestfor,
							assetdetails_requeststatus,assetdetails_assettfrgid,assetdetails_assetsalegid,assetdetails_not5k,assetdetails_assetowner,assetdetails_lease_startdate,
							assetdetails_lease_enddate,assetdetails_impairassetgid,assetdetails_impairasset,assetdetails_writeoffgid,assetdetails_assetcatchangegid,assetdetails_assetvaluegid,
							assetdetails_assetcapdategid,assetdetails_assetsplitgid,assetdetails_assetmergegid,assetdetails_assetcatchangedate,assetdetails_reducedvalue,
							assetdetails_branchgid,assetdetails_deponhold,assetdetails_deprate,assetdetails_parentgid,assetdetails_assetserialno,assetdetails_invoicegid,
							assetdetails_inwheadergid,assetdetails_inwdetailgid,assetdetails_inwarddate,assetdetails_mepno,assetdetails_ponum,assetdetails_crnum,
							assetdetails_imagepath,assetdetails_vendorname,assetdetails_trangid,assetdetails_isactive,assetdetails_isremoved,entity_gid,create_by)
								(select ''',@New_Asset_Id,''',assetdetails_qty,assetdetails_barcode,assetdetails_date,assetdetails_assetgroupid,assetdetails_assetcatgid,
								assetdetails_cat,assetdetails_subcat,assetdetails_productgid,assetdetails_value,assetdetails_cost,assetdetails_description,assetdetails_capdate,
								assetdetails_source,''',@ls_Status,''',''',@ls_Request_For,''',''',@ls_Request_Status,''',assetdetails_assettfrgid,
								assetdetails_assetsalegid,assetdetails_not5k,assetdetails_assetowner,assetdetails_lease_startdate,
								assetdetails_lease_enddate,assetdetails_impairassetgid,assetdetails_impairasset,
								assetdetails_writeoffgid,assetdetails_assetcatchangegid,assetdetails_assetvaluegid,assetdetails_assetcapdategid,	assetdetails_assetsplitgid,
								assetdetails_assetmergegid,assetdetails_assetcatchangedate,assetdetails_reducedvalue,
								''',@Asset_TFR_To,''',assetdetails_deponhold,assetdetails_deprate,assetdetails_parentgid,assetdetails_assetserialno,
								assetdetails_invoicegid,assetdetails_inwheadergid,assetdetails_inwdetailgid,assetdetails_inwarddate,assetdetails_mepno,
								assetdetails_ponum,assetdetails_crnum,assetdetails_imagepath,assetdetails_vendorname,assetdetails_gid,assetdetails_isactive,
								assetdetails_isremoved,entity_gid,create_by
								from fa_trn_tassetdetails  where assetdetails_gid in (',@Asset_Detail_Gids,')
								)
						 ');

								set @Insert_query = Query_Insert;
								#SELECT @Insert_query;
								PREPARE stmt FROM @Insert_query;
								EXECUTE stmt;
								set countRow = (select ROW_COUNT());
								DEALLOCATE PREPARE stmt;

                              if countRow > 0 then
									set Message = 'SUCCESS';
                                    select LAST_INSERT_ID() into @New_Asset_Id;
                               else
                                    set Message = 'FAIL';
                              End if;



			set @ls_Status = 'SUBMITTED';

					set Query_Insert = '';
					set Query_Insert = concat('
							INSERT INTO fa_trn_tassettfr
									(assettfr_assetdetailsid, assettfr_date,
                                     assettfr_from, assettfr_to,
                                     assettfr_status, assettfr_reason,
                                     assettfr_value, assettfr_newassetdetailsid,
                                     entity_gid,create_by)
							(select assetdetails_id,curdate(),
									assetdetails_branchgid,''',@Asset_TFR_To,''',
									''',@ls_Status,''',''',@Asset_TFR_Reason,''',
									assetdetails_value,''',@New_Asset_Id,''',
                                    entity_gid,''',ls_Createby,'''
							from fa_trn_tassetdetails
							where assetdetails_gid in (',@Asset_Detail_Gids,')
								 )');

							set @Insert_query = Query_Insert;
							#SELECT @Insert_query;
							PREPARE stmt FROM @Insert_query;
							EXECUTE stmt;
							set countRow = (select ROW_COUNT());
							DEALLOCATE PREPARE stmt;

                              if countRow > 0 then
                                  select LAST_INSERT_ID() into @Asset_TFR_Maxgid ;

                                  #### Update im Tmp Table
                                  set sql_safe_updates = 0;
                                  Update fa_tmp_tassetdetails set assetdetails_assettfrgid = @Asset_TFR_Maxgid
                                  where assetdetails_trangid = @Asset_Detail_Gids;

                                  set countRow = (select ROW_COUNT());

										if  countRow <= 0 then
											set Message = 'FAIL On Asset Temp Data Update.';
                                            leave sp_FA_TFR_Asset_Set;
                                        End if;


									set Message = 'SUCCESS';

						call sp_Trans_Set('Insert','FA_TRANSFER',@Asset_TFR_Maxgid,'NEW',
										  'G','MAKER',@Asset_TFR_Reason,@Entity_Gid,ls_Createby,@message);
									select @message into @tran;
									#select @message; #remove it
									if @tran <>0 or @tran <> '' then
											set Message = 'SUCCESS';
									else
											set Message = 'FAIL in tran';
											leave sp_FA_TFR_Asset_Set;
									end if;
                               else
                                    set Message = 'FAIL';
                              End if;

      End if;


  elseif ls_Type = 'TFR_CHECKER' and  ls_Sub_Type = 'UPDATE' then
         if ls_Action = 'UPDATE' then

				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_TFR_Gid'))) into @Asset_TFR_Gid;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_TFR_Status'))) into @Asset_TFR_Status;

                if @Asset_TFR_Gid is null or cast(@Asset_TFR_Gid as decimal(16,2))  = 0 then
						set Message = 'Asset_TFR_Gid Is Needed.';
                        leave sp_FA_TFR_Asset_Set;
                End if;

                if @Asset_TFR_Status is null or @Asset_TFR_Status = '' then
						set Message = 'Asset_TFR_Status Is Needed.';
                        leave sp_FA_TFR_Asset_Set;
                End if;

               set Query_Update = '';
               set Query_Update = concat('Update fa_trn_tassettfr
											  set assettfr_status = ''',@Asset_TFR_Status,''' ,
												  update_by = ''',ls_Createby,''' ,
                                                  update_date = current_timestamp()
											  Where assettfr_gid = ',@Asset_TFR_Gid,'
												  and entity_gid = ',@Entity_Gid,'
												');

									set @Query_Update = '';
								    set @Query_Update = Query_Update;
								    #select @Query_Update; ### Remove IT
									PREPARE stmt FROM @Query_Update;
									EXECUTE stmt;
									set countRow = (select ROW_COUNT());
									DEALLOCATE PREPARE stmt;

									if countRow <= 0 then
										set Message = 'Error On TFR Asset Update.';
										leave sp_FA_TFR_Asset_Set;
									 elseif    countRow > 0 then
										set Message = 'SUCCESS';
									End if;


         End if;
End if;


END