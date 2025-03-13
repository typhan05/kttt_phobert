import axiosInstance from "@/libs/axios";

interface Document {
  chude: string;
  filename: string;
  score: number;
}

type SearchResponse = {
  result: Document[]; // Adjust this type to match your API response
};

interface SearchParams {
  query: string;
}

export const searchService = {
  getSearch: async (params: SearchParams): Promise<SearchResponse> => {
    try {
      const response = await axiosInstance.get("/api/search", { params });
      return response.data;
    } catch (error) {
      console.error("Search API error:", error);
      throw new Error("Failed to fetch search results");
    }
  },
  getFileDownload: async (
    filename: string
  ): Promise<{ blob: Blob; filename: string }> => {
    try {
      const response = await axiosInstance.get("/api/download", {
        params: { filename }, // Send filename as query param
        responseType: "blob",
      });

      console.log({ response });

      // Extract filename from Content-Disposition header
      const contentDisposition = response.headers["content-disposition"];
      const extractedFilename = contentDisposition
        ? contentDisposition.split("filename=")[1]?.replace(/['"]/g, "") ||
          filename
        : filename;

      return { blob: response.data, filename: extractedFilename };
    } catch (error) {
      console.error("File download error:", error);
      throw new Error("Failed to download file");
    }
  },
};
