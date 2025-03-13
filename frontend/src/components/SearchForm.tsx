"use client";

import { searchService } from "@/services/searchService";
import React, { useState } from "react";

interface Document {
  chude: string;
  filename: string;
  score: number;
}

export default function SearchForm() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Document[]>();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const data = await searchService.getSearch({ query });
      setResults(data.result);

      console.log("Search results:", data.result);
    } catch (error) {
      console.error(error);
    }
  };

  const extractThreeDigits = (num: string) => {
    const match = num?.slice(0, 4); // Lấy 3 chữ số sau dấu phẩy
    return match;
  };

  return (
    <div className="max-w-3xl w-full mx-auto">
      <h2 className="text-3xl font-bold text-white text-center mb-8">
        Đề Tài: Nhóm 1
      </h2>
      <form
        onSubmit={handleSubmit}
        className="rounded-xl bg-gray-100 shadow-lg p-10 text-gray-800 relative overflow-hidden resize-x min-w-80"
      >
        <div className="relative mt-1">
          <input
            type="text"
            id="password"
            className="w-full pl-3 pr-10 py-2 border-2 border-gray-200 rounded-xl hover:border-gray-300 focus:outline-none focus:border-blue-500 transition-colors"
            placeholder="Search..."
            onChange={(e) => setQuery(e.target.value)}
          />
          <button
            className="block w-7 h-7 text-center text-xl leading-0 absolute top-2 right-2 text-gray-400 focus:outline-none hover:text-gray-900 transition-colors"
            type="submit"
          >
            <i className="mdi mdi-magnify" />
          </button>
        </div>
        <div className="absolute top-0 left-0 w-full h-2 flex">
          <div className="h-2 bg-blue-500 flex-1" />
          <div className="h-2 bg-red-500 flex-1" />
          <div className="h-2 bg-yellow-500 flex-1" />
          <div className="h-2 bg-blue-500 flex-1" />
          <div className="h-2 bg-green-500 flex-1" />
          <div className="h-2 bg-red-500 flex-1" />
        </div>
      </form>
      {results && results?.length > 0 && (
        <div className="border rounded-lg bg-white shadow-lg p-2 my-8 text-black">
          <h3 className="text-2xl font-semibold mb-4">Kết quả tìm kiếm</h3>
          {results?.map((item, idx) => {
            return (
              <div
                key={`search-item-${idx}`}
                className="border-b border-gray-300 last:border-b-0 py-1"
              >
                <p>
                  <b>Bài viết:</b> {item.filename}
                </p>
                <div className="flex gap-3">
                  <p>
                    <b>Danh Mục:</b> {item.chude}
                  </p>
                  <p>
                    <b>Độ tương đồng:</b>{" "}
                    {extractThreeDigits(String(item.score))}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
