CREATE DEFINER=`developer`@`%` PROCEDURE `sp_FAAssetCategory_Set`(IN `ls_Action` varchar(32),IN `ls_Type` varchar(32),
IN `ls_Sub_Type` varchar(32),IN `lj_Details` json,IN `lj_Classification` json,IN `ls_Createby` varchar(32),
OUT `Message` varchar(1024))
sp_FAAssetCategory:BEGIN

#### Bala Oct 25 2019
Declare errno int;
Declare msg varchar(1000);
Declare Query_Update varchar(1000);
Declare countRow int;
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
                    leave sp_FAAssetCategory;
             End if;


if ls_Type = 'ASSET_CAT' and  ls_Sub_Type = 'MST' and ls_Action = 'INSERT' then


             select JSON_LENGTH(lj_Details,'$') into @li_json_count_Details ;
             if @li_json_count_Details is  null or @li_json_count_Details = 0 or @li_json_count_Details = '' then
					set Message = 'No Data In lj_Details Json';
                    leave sp_FAAssetCategory;
             End if;


                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_SubCategory_Gid'))) into @AssetCat_SubCategory_Gid;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_SubCatName'))) into @AssetCat_SubCatName;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_LifeTime'))) into @Asset_LifeTime;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_DepType'))) into @Asset_DepType;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_DepRate'))) into @Asset_DepRate;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.AssetCat_Remarks'))) into @AssetCat_Remarks;



					if @AssetCat_SubCategory_Gid is  null or @AssetCat_SubCategory_Gid = '' then
						set Message = 'Asset_SubCategory_Gid Is Needed.';
						leave sp_FAAssetCategory;
					End if;

					if @AssetCat_SubCatName is  null or @AssetCat_SubCatName = '' then
						set Message = 'AssetCat_SubCatName Is Needed.';
						leave sp_FAAssetCategory;
					End if;

					if @Asset_LifeTime is  null or @Asset_LifeTime = '' then
						set Message = 'Asset_LifeTime Is Needed.';
						leave sp_FAAssetCategory;
					End if;

                    if @Asset_DepType is  null or @Asset_DepType = '' then
						set Message = 'Asset_DepType Is Needed.';
						leave sp_FAAssetCategory;
					End if;

					if @Asset_DepRate is  null or @Asset_DepRate = '' then
						set Message = 'Asset_DepRate Is Needed.';
						leave sp_FAAssetCategory;
					End if;

                    if @AssetCat_Remarks is  null or @AssetCat_Remarks = '' then
						set Message = 'AssetCat_Remarks Is Needed.';
						leave sp_FAAssetCategory;
					End if;


				set Query_Insert = '';
				set Query_Insert = concat('
							INSERT INTO fa_mst_tassetcat
									(assetcat_subcategorygid, assetcat_subcatname,
									 assetcat_lifetime, assetcat_deptype, assetcat_deprate,
									 assetcat_remarks,entity_gid,create_by)
							  values(',@AssetCat_SubCategory_Gid,',''',@AssetCat_SubCatName,''',
                                     ''',@Asset_LifeTime,''',''',@Asset_DepType,''',''',@Asset_DepRate,''',
                                     ''',@AssetCat_Remarks,''',',@Entity_Gid,',',ls_Createby,')');

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

      End if;

END