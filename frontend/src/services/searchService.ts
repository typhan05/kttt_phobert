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
};
