CREATE DEFINER=`developer`@`%` PROCEDURE `sp_FADepreciation_Set`(IN `ls_Action` varchar(32),IN `ls_Type` varchar(32),
IN `ls_Sub_Type` varchar(32),IN `lj_Details` json,IN `lj_Other` json,IN `lj_Classification` json,
IN `ls_Createby` varchar(16),OUT `Message` varchar(1024)
)
sp_FADepreciation_Set:BEGIN
#### Ramesh Nov 4 2019
Declare errno int;
Declare msg varchar(1000);
Declare i int;
Declare j int;
#Declare Query_Select varchar(2048);
Declare Query_Insert varchar(2018);
Declare countRow int;
#Declare AssetDetails_Gid varchar(2048);
# Null Selected Output
DECLARE done INT DEFAULT 0;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
#...

  DECLARE EXIT HANDLER FOR SQLEXCEPTION,sqlwarning

    BEGIN

     GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
     set Message = concat(errno , msg);
     ROLLBACK;
     END;

     select JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Gid[0]'))) into @Entity_Gid;

             if @Entity_Gid is  null or @Entity_Gid = 0 or @Entity_Gid = '' then
					set Message = 'Entity Gid Is Needed.';
                    leave sp_FADepreciation_Set;
             End if;

		select JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Gid[0]'))) into @Entity_Gid;

             if @Entity_Gid is  null or @Entity_Gid = 0 or @Entity_Gid = '' then
					set Message = 'Entity Gid Is Needed.';
                    leave sp_FADepreciation_Set;
             End if;

SET SESSION group_concat_max_len=4294967295;
if ls_Type = 'DEPRECATION' and ls_Sub_Type = 'REGULAR' then

			select JSON_LENGTH(lj_Details,'$') into @li_json_count_Details ;

                   if @li_json_count_Details is null or @li_json_count_Details = 0 then
						set Message = 'No Data In Json - data.';
						leave sp_FADepreciation_Set;
					end if;

                      select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Calculate_For'))) into @Deprecation_Calculate_For;
					  select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.From_Date'))) into @DepCalFrom_DateD;
					  select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.To_Date'))) into @DepCalTo_DateD;
                      select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.DepType'))) into @DepTypeD;

                      if @DepTypeD = 'REGULAR' then
							set @DepTypeD = '1';
                      End if;

                   # ### Validation

                      if @Deprecation_Calculate_For = 'ALL' then
							#### if for all . check that no data in TMP Table.
                            set @assetdetail_exist = 0 ;
                            Select ifnull(max(a.assetdetails_gid),0) into @assetdetail_exist from fa_tmp_tassetdetails as a
							where a.assetdetails_requestfor <> 'NEW' ;

                            if @assetdetail_exist <> 0 then
									set Message = 'Some Assets Are In Process.Deprecation Will Not Calculate.' ;
                                #    leave sp_FADepreciation_Set;
                            End if;

                      End if;

                      if @DepCalFrom_DateD is null or @DepCalFrom_DateD = '' then
						set Message = 'Depreciation From Date Is Needed.';
                        leave sp_FADepreciation_Set;
                      End if;

                      if @DepCalTo_DateD is null or @DepCalTo_DateD = '' then
						set Message = 'Depreciation To Date Is Needed.';
                        leave sp_FADepreciation_Set;
                      End if;

                      #### Know the Number of Days.
                      select datediff(@DepCalTo_DateD,@DepCalFrom_DateD) into @DepDaysD ;
                      select date_format(@DepCalTo_DateD,'%m') into @DepMonthD ;
                      select date_format(@DepCalTo_DateD,'%Y') into @DepYearD ;
                      #

								Select ifnull(concat('[',group_concat(json_object('asset_gid',a.assetdetails_gid,'asset_cost',a.assetdetails_cost,
                                'asset_value',a.assetdetails_value,'asset_cpdate',a.assetdetails_capdate,'asset_deptype',b.assetcat_deptype,
                                'asset_deprate',b.assetcat_deprate,'asset_lifetime',b.assetcat_lifetime)),']'),'{}')
									into @lj_assetDataD
								 from fa_trn_tassetdetails as a
								 inner join fa_mst_tassetcat as b on b.assetcat_gid = a.assetdetails_assetcatgid
								where a.assetdetails_deponhold = 'N' and a.assetdetails_status = 'ACTIVE'
								and  a.assetdetails_isactive = 'Y' and a.assetdetails_isremoved = 'N'
								and b.assetcat_isactive = 'Y' and b.assetcat_isremoved = 'N'
                                ;
                                ### TO DO New Column - Asset Life Time
                                #### Validation as per test cases  :: TO DO

                                select JSON_LENGTH(@lj_assetDataD,'$') into @asset_countD ;

                                if @asset_countD = 0 or @asset_countD is null then
									set Message = 'No Asset Data To Deprecation.';
                                    rollback;
                                    leave sp_FADepreciation_Set;
                                End if;

                                set i = 0;

                                While i <= @asset_countD -1 DO

                                       select JSON_UNQUOTE(JSON_EXTRACT(@lj_assetDataD,CONCAT('$[',i,'].asset_gid'))) into @asset_gidD;
                                       select JSON_UNQUOTE(JSON_EXTRACT(@lj_assetDataD,CONCAT('$[',i,'].asset_cost'))) into @asset_costD;
                                       select JSON_UNQUOTE(JSON_EXTRACT(@lj_assetDataD,CONCAT('$[',i,'].asset_value'))) into @asset_valueD;
                                       select JSON_UNQUOTE(JSON_EXTRACT(@lj_assetDataD,CONCAT('$[',i,'].asset_cpdate'))) into @asset_cpdateD;
                                       select JSON_UNQUOTE(JSON_EXTRACT(@lj_assetDataD,CONCAT('$[',i,'].asset_deptype'))) into @asset_deptypeD;
                                       select JSON_UNQUOTE(JSON_EXTRACT(@lj_assetDataD,CONCAT('$[',i,'].asset_deprate'))) into @asset_deprateD;
                                       select JSON_UNQUOTE(JSON_EXTRACT(@lj_assetDataD,CONCAT('$[',i,'].asset_lifetime'))) into @asset_lifetimeD;

                                       #### Know the Last Deprecation date
                                       set @Last_depDateD = '';
                                       Select ifnull(max(depreciation_todate) ,'') into @Last_depDateD
										from fa_trn_tdepreciation
										where depreciation_assetdetailsgid = @asset_gidD and depreciation_isactive = 'Y' and depreciation_isremoved = 'N' ;

                                      if @Last_depDateD <> '' and @Last_depDateD is not null then
											if @DepCalFrom_DateD <= @Last_depDateD then
													set Message = 'Already Depreciation Run For The Asset.';
                                                    #rollback;
                                                    #leave sp_FADepreciation_Set;
                                            End if;
                                      End if;

                                      if @asset_deptypeD = 'SLM' then
                                         ### Get Rate Per Day
                                         set @DepValuePerDay = ((@asset_costD * @asset_deprateD) / 100)/365;
                                         set @DepValueTotalD = @DepDaysD * @DepValuePerDay;
                                         set @DepValueTotalD = cast(@DepValueTotalD as decimal(16,2));

									elseif @asset_deptypeD = 'WDV' then
                                            set @DepValuePerDay = ((@asset_valueD * @asset_deprateD) / 100)/365;
											set @DepValueTotalD = @DepDaysD * @DepValuePerDay;      ### TO DO Update
											set @DepValueTotalD = cast(@DepValueTotalD as decimal(16,2));
                                     else
                                         set Message = 'Error On Depreciation Type.';
                                         leave sp_FADepreciation_Set;
									End if;

                                    #select @asset_valueD,@asset_deprateD,@DepValueTotalD;
                                    #leave sp_FADepreciation_Set;

                                      ### Insert Process
                                      #select @asset_gidD,@DepCalFrom_DateD,@DepCalTo_DateD,@DepMonthD,@DepYearD,@DepValueTotalD,@DepTypeD,@Entity_Gid,ls_Createby;

										set Query_Insert = '';
                                        set Query_Insert = concat('Insert into fa_trn_tdepreciation (depreciation_assetdetailsgid,depreciation_fromdate,depreciation_todate,depreciation_month,
																					depreciation_year,depreciation_value,depreciation_type,entity_gid,create_by
																					) values (''',@asset_gidD,''',''',@DepCalFrom_DateD,''',''',@DepCalTo_DateD,''',''',@DepMonthD,''',
                                                                                    ''',@DepYearD,''',''',@DepValueTotalD,''',''',@DepTypeD,''',''',@Entity_Gid,''',''',ls_Createby,''')
																					');

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
													  End if;

                                                      UPDATE fa_trn_tassetdetails SET assetdetails_cost = assetdetails_cost - cast(@DepValueTotalD as decimal(16,2))
                                                      WHERE assetdetails_gid = @asset_gidD;



                                       set i = i+1;
                                End While;



End if;


END