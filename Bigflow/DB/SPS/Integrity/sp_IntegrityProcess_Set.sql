CREATE DEFINER=`developer`@`%` PROCEDURE `sp_IntegrityProcess_Set`(in ls_Action varchar(16),
in ls_Type varchar(32),
in lj_data json,
in lj_file json,
in lj_classification json,
in li_create_by int,
out Message varchar(1000))
sp_IntegrityProcess_set:BEGIN
#Aswani,vignesh created on 03-01-2020
	 declare ls_count varchar(2000);
	 declare i,j varchar(200);
	 declare Query_Insert varchar(1000);
     declare Query_Update varchar(9000);
     declare Query_column varchar(1000);
     declare Query_value varchar(1000);
     declare errno int;
     declare msg varchar(1000);
     declare vali_Date varchar(32);
     declare update_count int;
     declare countRow int;
  DECLARE done INT DEFAULT 0;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
 #...
	 DECLARE EXIT HANDLER FOR SQLEXCEPTION,sqlwarning
     BEGIN

     GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
     set Message = concat(errno , msg);
     ROLLBACK;
     END;
	 start transaction;

select fn_Classification('ENTITY_ONLY',lj_Classification) into @OutMsg_Classification ;
select  JSON_UNQUOTE(JSON_EXTRACT(@OutMsg_Classification, '$.Entity_Gid[0]')) into @Entity_Gids;
if @Entity_Gids is  null or @Entity_Gids = '' then
		select  JSON_UNQUOTE(JSON_EXTRACT(@OutMsg_Classification, '$.Message')) into @Message;
		set Message = concat('Error On Classification Data - ',@Message);
		leave sp_IntegrityProcess_set;
End if;



if ls_Action='Insert' and ls_Type = 'Integrity_Upload' then

	   select JSON_LENGTH(lj_file,'$.FILE')into @li_json_File_count;
		  if @li_json_File_count is null or @li_json_File_count =0 then
			   set message ='no File In Json - file';
			   rollback;
			   leave sp_IntegrityProcess_set;
		   end if;

			select JSON_UNQUOTE(JSON_EXTRACT(lj_data,CONCAT('$.Bank_Gid[0]'))) into @bank_gid;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Entity_Gid[0]'))) into @entity_gid;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_file,CONCAT('$.FILE.File_Gid[0]'))) into @file_Id;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_file,CONCAT('$.FILE.File_Name[0]'))) into @file_Name;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_file,CONCAT('$.FILE.File_Path[0]'))) into @file_Path;

     call sp_File_Set('Insert','a',@file_Id,@file_Name,@file_Path,
                        lj_classification, '{}',li_create_by ,@Message);

			select @Message into @Out_msg_BankStmt;

             SET @Out_msg_BankStmt_Message = (SELECT SPLIT_STR((@Out_msg_BankStmt), ',', 2));

				if @Out_msg_BankStmt_Message= 'SUCCESS' then
				  set @Out_msg_BankStmt_id = (SELECT SPLIT_STR((@Out_msg_BankStmt), ',', 1));
				  set @File_gid = @Out_msg_BankStmt_id;
				end if;

			  if @File_gid = ''  then
                         set Message = ' No file_gid Gid';
                         leave sp_IntegrityProcess_Set;
			  end if;


				select JSON_LENGTH(lj_data,'$') into @li_jsoncount;
				#select JSON_LENGTH(lj_classification,'$') into @li_classification_jsoncount;
				 if @li_jsoncount='' or @li_jsoncount is null then
				 set message='NO DATA IN JSON-SP_Intergrity_Set.';
                 rollback;
				 leave sp_IntegrityProcess_Set;
			  end if;

			 # if @li_classification_jsoncount='' or @li_classification_jsoncount is null then
				# set message='NO DATA IN JSON-SP_Intergrity_Set.';
                 #rollback;
				 #leave sp_IntegrityProcess_Set;
			  #end if;

              #Select JSON_UNQUOTE(JSON_EXTRACT(lj_data,CONCAT('$.exceldump_filegid')))into @exceldump_filegid;
              Select JSON_UNQUOTE(JSON_EXTRACT(lj_data,CONCAT('$.exceldump_templateheadergid')))into @exceldump_templateheadergid;
              Select JSON_UNQUOTE(JSON_EXTRACT(lj_data,CONCAT('$.exceldump_error')))into @exceldump_error;
              Select JSON_UNQUOTE(JSON_EXTRACT(lj_data,CONCAT('$.exceldump_status')))into @exceldump_status;
             # Select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.entity_gid')))into @entity_gid;
             # Select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.create_by')))into @create_by;

		select JSON_LENGTH(lj_data,'$.INTRA') into @ls_filter_count;
          #select @ls_filter_count;

		set i=0;
		while i<@ls_filter_count do
							Select JSON_UNQUOTE(JSON_EXTRACT(lj_data,CONCAT('$.INTRA[',i,'].GL_NUMBER')))into @GL_NUMBER;
							Select JSON_UNQUOTE(JSON_EXTRACT(lj_data,CONCAT('$.INTRA[',i,'].DATE')))into @date1;
							Select JSON_UNQUOTE(JSON_EXTRACT(lj_data,CONCAT('$.INTRA[',i,'].DESCRIPTION')))into @DESCRIPTION;
                            Select JSON_UNQUOTE(JSON_EXTRACT(lj_data,CONCAT('$.INTRA[',i,'].INVOICE_NUMBER')))into @INVOICE_NUMBER;
                            Select JSON_UNQUOTE(JSON_EXTRACT(lj_data,CONCAT('$.INTRA[',i,'].AMOUNT')))into @AMOUNT;
							#Select JSON_UNQUOTE(JSON_EXTRACT(ls_filter,CONCAT('$.INTRA[',i,'].exceldump_filegid')))into @entry_period;


                             set @date1=date_format(@date1,'%Y-%m-%d');



							select group_concat(templatedetails_exceldumpcol)into @concatexcelcol from gal_mst_ttemplatedetails
                            inner join gal_mst_ttemplateheader ON  templatedetails_templateheadergid=templateheader_gid
                            where templatedetails_templateheadergid=@exceldump_templateheadergid;

                             set Query_column=concat(',',@concatexcelcol);

          #select @GL_NUMBER,@date1,@DESCRIPTION,@INVOICE_NUMBER,@AMOUNT;
         # select Query_column, @File_gid,@exceldump_templateheadergid,@exceldump_error,
			#	 @exceldump_status,@Entity_Gids,li_create_by,@GL_NUMBER,@date1,@DESCRIPTION,@INVOICE_NUMBER,@AMOUNT;

          set Query_Insert = '';
					set Query_Insert = concat('Insert into gal_mst_texceldump (exceldump_filegid,
												exceldump_templateheadergid,exceldump_error,
												exceldump_status,entity_gid, create_by',Query_column,')
                                                Values(',@File_gid,',',@exceldump_templateheadergid,',
													   ''',@exceldump_error,''',''',@exceldump_status,''',',@Entity_Gids,',
                                                       ',li_create_by,',''',@GL_NUMBER,''',''',@date1,''',''',@DESCRIPTION,''',''',@INVOICE_NUMBER,''',''',@AMOUNT,'''

                                                      )' );

								set @Insert_query = Query_Insert;
								#SELECT @Insert_query;
								PREPARE stmt FROM @Insert_query;
								EXECUTE stmt;
								set countRow = (select ROW_COUNT());
								DEALLOCATE PREPARE stmt;


		   set i=i+1;
        end while;

					if countRow > 0 then
							set Message ='SUCCESS';
						commit;
						else
							set Message = 'FAIL';
							rollback;
                            leave sp_IntegrityProcess_set;
						end if;


    end if;

END