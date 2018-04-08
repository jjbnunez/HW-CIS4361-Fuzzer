#include <stdio.h>
#include <malloc.h>
#include <string.h>

typedef int                 BOOL;
typedef unsigned char       BYTE;
typedef unsigned short      WORD;
typedef unsigned long       DWORD;

#define FALSE               0
#define TRUE                1

WORD  SwapEndian(WORD S);
DWORD GetFileSize(FILE *fp);
BOOL  CopyStream(FILE *Src,FILE *Dest);
BOOL  GetJPEGSize(FILE *JPGStream,WORD *AWidth,WORD *AHeight,BOOL *CMYK);
void  Write_CrossReferenceTable(FILE *AStream,DWORD ObjectPosArray[],int Count);
void  Write_ContentsObject(FILE *AStream,DWORD ObjectPosArray[],int *ObjectIndex,int w,int h);
int   JPGtoPDF(const char *OpenName,const char *SaveName);

int main(int argc,char *argv[])
{
   if (argc >= 2)
     return (JPGtoPDF(argv[1],"jpg2pdf.pdf"));
   else
   {
     printf("Not Found!\n");
     return(0);
   }
}

WORD SwapEndian(WORD S)
{
 return ((S & 0x00FF) << 8) | ((S & 0xFF00) >> 8)  ;
}

DWORD GetFileSize(FILE *fp)
{
 int Pos;
 DWORD Size;
 
 Pos =ftell(fp);
 fseek(fp, 0, SEEK_END );    
 Size = ftell(fp);    
 fseek(fp, Pos, SEEK_SET );
 return Size;
}

BOOL CopyStream(FILE *Src,FILE *Dest)
{
 BYTE  *buffer;
 int   Pos;
 DWORD FileSize;

 Pos =ftell(Src);
 FileSize=GetFileSize(Src);

 buffer=(BYTE *)malloc(FileSize);
 if (buffer==NULL) 
   return FALSE;
 fseek(Src,0,SEEK_SET);
 fread(buffer,1,FileSize,Src);       
 fwrite(buffer,1,FileSize,Dest);
 free(buffer);

 fseek(Src,Pos,SEEK_SET);
 return TRUE;
}

BOOL GetJPEGSize(FILE *JPGStream,WORD *AWidth,WORD *AHeight,BOOL *CMYK)
{
 WORD wrk;
 BYTE Sampling;

 WORD SOF0 =0xFFC0; /* Normal */
 WORD SOF2 =0xFFC2; /* Progressive */

 /* JFIF */
 if (fread(&wrk,2,1,JPGStream)<1) 
   return FALSE;

 if (SwapEndian(wrk)!=0xFFD8)
    return FALSE;      

 while (1)
 {
     if (fread(&wrk,2,1,JPGStream)<1) 
       return FALSE;
     wrk=SwapEndian(wrk);
     
     /* JPEG Maker */
     if ((wrk==SOF0) | (wrk==SOF2))
     {  
        /* Skip Segment Length  */
        if (fseek(JPGStream,ftell(JPGStream)+2,SEEK_SET)) 
         return FALSE;

        /* Skip Sample */
        if (fseek(JPGStream,ftell(JPGStream)+1,SEEK_SET)) 
         return FALSE;

        /* Height */
        if (fread(&wrk,2,1,JPGStream)<1) 
          return FALSE;
        *AHeight=SwapEndian(wrk);

        /* Width */          
        if (fread(&wrk,2,1,JPGStream)<1) 
         return FALSE;
        *AWidth=SwapEndian(wrk);
        
        /* ColorMode */
        if (fread(&Sampling,1,1,JPGStream)<1) 
          return FALSE;
        
        switch (Sampling)
        {
          case 3  : *CMYK = FALSE; break; /* RGB  */
          case 4  : *CMYK = TRUE ; break; /* CMYK */
          default : return FALSE;         /* ???  */ 
        }

        return TRUE; 
     }
     else if ((wrk==0xFFFF) | (wrk==0xFFD9))
     {
         return FALSE;  
     }

     /* Skip Segment */  
     if (fread(&wrk,2,1,JPGStream)<1) 
       return FALSE;
     
     if (fseek(JPGStream,ftell(JPGStream)+SwapEndian(wrk)-2,SEEK_SET )) 
       return FALSE;
 }
}

void Write_CrossReferenceTable(FILE *AStream,DWORD ObjectPosArray[],int Count)
{
   int i;

   fprintf(AStream,"xref\n");
   fprintf(AStream,"0 %d\n",Count+1);
   fprintf(AStream,"0000000000 65535 f \n");

   for (i= 0; i<=Count-1;i++)
      fprintf(AStream,"%0.10d 00000 n \n",ObjectPosArray[i]);
}

void Write_ContentsObject(FILE *AStream,DWORD ObjectPosArray[],int *ObjectIndex,int w,int h)
{
   int Length;

   /* Contents */
   ObjectPosArray[*ObjectIndex]  =(DWORD)ftell(AStream);
     fprintf(AStream,"%d 0 obj\n",*ObjectIndex+1);
     fprintf(AStream,"<< /Length %d 0 R >>\n",*ObjectIndex+2);
     fprintf(AStream,"stream\n");

        /* stream */
        Length=ftell(AStream);
          fprintf(AStream,"q\n");
          fprintf(AStream,"%d 0 0 %d 0 0 cm\n",w,h);
          fprintf(AStream,"/Im0 Do\n");
          fprintf(AStream,"Q\n");
        Length=ftell(AStream)-Length;

     fprintf(AStream,"endstream\n");
     fprintf(AStream,"endobj\n");
   *ObjectIndex=*ObjectIndex+1;

   /* stream Length */
   ObjectPosArray[*ObjectIndex] =(DWORD)ftell(AStream);
     fprintf(AStream,"%d 0 obj\n",*ObjectIndex+1);
     fprintf(AStream,"%d\n",Length);
     fprintf(AStream,"endobj\n");
   *ObjectIndex=*ObjectIndex+1;
}

int JPGtoPDF(const char *OpenName,const char *SaveName)
{
 BOOL  cmyk; 
 WORD  w,h;
 int   ObjectIndex;
 DWORD ObjectPosArray[10];
 FILE  *JPGStream,*AStream; 

    ObjectIndex=0;

    /* Open Jpeg File */
    JPGStream=fopen(OpenName,"rb");
    if(JPGStream==NULL)
    {
       printf("Error : Can not Open File.\n");
       return(-1);  
    }

    /* Get JPEG size */
    if (GetJPEGSize(JPGStream,&w,&h,&cmyk)==FALSE)
    {
       printf("Error : Can not get JPEG size.\n");
       return(-1);  
    }

    /* Create PDF File */
    AStream=fopen(SaveName,"wb+");
    if(AStream==NULL)
    {
        printf("Error : Can not Create File.\n");
        fclose(JPGStream);
        return(-1); 
    }

    /* ------------------------------------------------------------- */
    /*  Writting PDF                                                 */
    /* ------------------------------------------------------------- */

    /* PDF version */
    fprintf(AStream,"%%PDF-1.2\n");

    /* Catalog */
    ObjectPosArray[ObjectIndex] =ftell(AStream);
      fprintf(AStream,"%d 0 obj\n",ObjectIndex+1);
      fprintf(AStream,"<<\n");
      fprintf(AStream,"/Type /Catalog\n");
      fprintf(AStream,"/Pages 2 0 R\n");
      /* View Option (100%) */
      /*fprintf(AStream,"/OpenAction [3 0 R /XYZ -32768 -32768 1 ]\n"); */
      fprintf(AStream,">>\n");
      fprintf(AStream,"endobj\n");
    ObjectIndex++;

     /* Parent Pages */
     ObjectPosArray[ObjectIndex] =ftell(AStream);
       fprintf(AStream,"%d 0 obj\n",ObjectIndex+1);
       fprintf(AStream,"<<\n");
       fprintf(AStream,"/Type /Pages\n");
       fprintf(AStream,"/Kids [ 3 0 R ]\n");
       fprintf(AStream,"/Count 1\n");
       fprintf(AStream,">>\n");
       fprintf(AStream,"endobj\n");
     ObjectIndex++;

     /* Kids Page */
     ObjectPosArray[ObjectIndex] =ftell(AStream);
       fprintf(AStream,"%d 0 obj\n",ObjectIndex+1);
       fprintf(AStream,"<<\n");
       fprintf(AStream,"/Type /Page\n");
       fprintf(AStream,"/Parent 2 0 R\n");
       fprintf(AStream,"/Resources\n");
       fprintf(AStream,"<<\n");
       fprintf(AStream,"/XObject << /Im0 4 0 R >>\n");
       fprintf(AStream,"/ProcSet [ /PDF /ImageC ]\n");
       fprintf(AStream,">>\n");
       fprintf(AStream,"/MediaBox [ 0 0 %d %d ]\n",w,h);
       fprintf(AStream,"/Contents 5 0 R\n");
       fprintf(AStream,">>\n");
       fprintf(AStream,"endobj\n");
     ObjectIndex++;

     /* XObject Resource */
     ObjectPosArray[ObjectIndex] =ftell(AStream); 
       fprintf(AStream,"%d 0 obj\n",ObjectIndex+1);

       fprintf(AStream,"<<\n");
       fprintf(AStream,"/Type /XObject\n");
       fprintf(AStream,"/Subtype /Image\n");
       fprintf(AStream,"/Name /Im0\n");
       fprintf(AStream,"/Width %d\n",w);
       fprintf(AStream,"/Height %d\n",h);
       fprintf(AStream,"/BitsPerComponent 8\n");
       fprintf(AStream,"/Filter [/DCTDecode]\n");
       if (cmyk==FALSE)
         fprintf(AStream,"/ColorSpace /DeviceRGB\n");
       else
       {
         fprintf(AStream,"/ColorSpace /DeviceCMYK\n");
         fprintf(AStream,"/Decode[1 0 1 0 1 0 1 0]\n"); /* Photoshop CMYK (NOT BIT) */
       }
       fprintf(AStream,"/Length %d >>\n",GetFileSize(JPGStream));
       fprintf(AStream,"stream\n");       
       if (CopyStream(JPGStream,AStream)==FALSE)
       {
          printf("Error : No Memory \n");
          return(-1);
       }
       fprintf(AStream,"endstream\n");
       fprintf(AStream,"endobj\n");
     ObjectIndex++;

    /* Contents Stream & Object */
    Write_ContentsObject(AStream,ObjectPosArray,&ObjectIndex,w,h);

    /* CrossReferenceTable */
    ObjectPosArray[ObjectIndex] =ftell(AStream);
    Write_CrossReferenceTable(AStream,ObjectPosArray,(int)ObjectIndex);

    /* trailer */
    fprintf(AStream,"trailer\n");
    fprintf(AStream,"<<\n");
    fprintf(AStream,"/Size %d\n",ObjectIndex+1);
    fprintf(AStream,"/Root 1 0 R\n");
    fprintf(AStream,">>\n");
    fprintf(AStream,"startxref\n");
    fprintf(AStream,"%d\n",ObjectPosArray[ObjectIndex]);
    fprintf(AStream,"%%%%EOF\n");

    fclose(JPGStream); fclose(AStream);

    printf("\nSuccess!\n");

    return (0);
}
